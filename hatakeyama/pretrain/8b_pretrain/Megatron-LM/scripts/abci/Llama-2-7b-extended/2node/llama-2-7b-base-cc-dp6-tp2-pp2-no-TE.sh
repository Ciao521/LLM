#!/bin/bash
#$ -l rt_AF=3
#$ -l h_rt=7:00:00:00
#$ -j y
#$ -o outputs/llama-2-7b-base/2node/
#$ -cwd

# module load
source /etc/profile.d/modules.sh
module load cuda/12.1/12.1.1
module load cudnn/8.9/8.9.5
module load nccl/2.18/2.18.3-1
module load hpcx/2.12

# python virtualenv
source .env/bin/activate

# distributed settings
export MASTER_ADDR=$(/usr/sbin/ip a show dev bond0 | grep 'inet ' | awk '{ print $2 }' | cut -d "/" -f 1)
export MASTER_PORT=$((10000 + ($JOB_ID % 50000)))

echo "MASTER_ADDR=${MASTER_ADDR}"

# hostfile

if [[ "$SGE_RESOURCE_TYPE" == "rt_F" ]]; then
  export NUM_GPU_PER_NODE=4
  NODE_TYPE="v100"
elif [[ "$SGE_RESOURCE_TYPE" == "rt_AF" ]]; then
  export NUM_GPU_PER_NODE=8
  NODE_TYPE="a100"
else
  echo "Unrecognized SGE_RESOURCE_TYPE: $SGE_RESOURCE_TYPE"
fi

NUM_NODES=$NHOSTS
NUM_GPUS=$((${NUM_NODES} * ${NUM_GPU_PER_NODE}))

mkdir -p ./hostfile

HOSTFILE_NAME=./hostfile/hostfile_${JOB_ID}
while read -r line; do
  echo "${line} slots=${NUM_GPU_PER_NODE}"
done <"$SGE_JOB_HOSTLIST" >"$HOSTFILE_NAME"

# model config
# llama-2-7b: https://huggingface.co/meta-llama/Llama-2-7b-hf/blob/main/config.json
HIDDEN_SIZE=4096
FFN_HIDDEN_SIZE=11008 # intermediate size (HuggingFace)
NUM_LAYERS=32
NUM_HEADS=32
SEQ_LENGTH=4096

# distributed settings
TENSOR_PARALLEL_SIZE=2   # fixed
PIPELINE_PARALLEL_SIZE=2 # num layers 32: Llama-2 7B
DATA_PARALLEL_SIZE=$((${NUM_GPUS} / (${TENSOR_PARALLEL_SIZE} * ${PIPELINE_PARALLEL_SIZE})))

# training config
MICRO_BATCH_SIZE=1
GLOBAL_BATCH_SIZE=1620
TRAIN_STEPS=25000 # e.g. llama: 1T tokens / 4M tokens_per_batch = 250000 steps
# 今回は約100B Tokensなので 1/10

LR=1e-4
MIN_LR=3.3e-6
LR_WARMUP_STEPS=1000
WEIGHT_DECAY=0.1
GRAD_CLIP=1

# model config
TOKENIZER_MODEL=/bb/llm/gaf51275/llama/huggingface-checkpoint/Llama-2-7b-hf/tokenizer.model
CHECKPOINT_DIR=/bb/llm/gaf51275/llama/llama-megatron-convert-checkpoint-hf/Llama-2-7b/tp${TENSOR_PARALLEL_SIZE}-pp${PIPELINE_PARALLEL_SIZE}
CHECKPOINT_SAVE_DIR=/groups/gaf51275/llm-jp/checkpoints/megatron-lm/llama-2-7b-base-megatron/okazaki_lab_cc/tp${TENSOR_PARALLEL_SIZE}-pp${PIPELINE_PARALLEL_SIZE}

mkdir -p ${CHECKPOINT_SAVE_DIR}

# data config
DATASET_DIR=/bb/llm/gaf51275/llama/datasets/okazaki_lab_cc_1500_okazaki_lab_cc_original

DATA_PATH=""

# ja okazaki lab common crawl
DATA_PATH="${DATA_PATH} 10414138710 ${DATASET_DIR}/split_0_text_document"
DATA_PATH="${DATA_PATH} 10310340698 ${DATASET_DIR}/split_1_text_document"
DATA_PATH="${DATA_PATH} 12327844508 ${DATASET_DIR}/split_2_text_document"
DATA_PATH="${DATA_PATH} 16269817007 ${DATASET_DIR}/split_3_text_document"
DATA_PATH="${DATA_PATH} 38018807005 ${DATASET_DIR}/split_4_text_document"

# ja wikipedia
DATA_PATH="${DATA_PATH} 2659052072 ${DATASET_DIR}/ja_wiki_merged_train_text_document"

# en arxiv
DATA_PATH="${DATA_PATH} 5000000000 ${DATASET_DIR}/lumi_en_arxiv_merged_text_document"

# en falcon refined-web
DATA_PATH="${DATA_PATH} 5000000000 ${DATASET_DIR}/lumi_en_falcon_merged_threadripper-3960x_8_text_document"

# job name
JOB_NAME="llama-2-7b-base-okazaki-lab-cc-${NODE_TYPE}-${NUM_NODES}node-${NUM_GPUS}gpu-${SEQ_LENGTH}s-DP=${DATA_PARALLEL_SIZE}-TP=${TENSOR_PARALLEL_SIZE}-PP=${PIPELINE_PARALLEL_SIZE}-BS=${GLOBAL_BATCH_SIZE}-LR=${LR}-MINLR=${MIN_LR}-WARMUP=${LR_WARMUP_STEPS}-WD=${WEIGHT_DECAY}-GC=${GRAD_CLIP}"

# --norm-epsilon 1e-5 : conifg.json (RMS norm)

# checkpoint load
if [[ -f "${CHECKPOINT_SAVE_DIR}/latest_checkpointed_iteration.txt" ]]; then
  # resume training
  CHECKPOINT_ARGS="--load ${CHECKPOINT_SAVE_DIR}"
else
  # first training
  CHECKPOINT_ARGS="--load ${CHECKPOINT_DIR} --no-load-rng --no-load-optim"
fi

# run
mpirun -np $NUM_GPUS \
  --npernode $NUM_GPU_PER_NODE \
  -hostfile $HOSTFILE_NAME \
  -x MASTER_ADDR=$MASTER_ADDR \
  -x MASTER_PORT=$MASTER_PORT \
  -x CUDA_DEVICE_MAX_CONNECTIONS=1 \
  -bind-to none -map-by slot \
  -x PATH \
  python pretrain_gpt.py \
  --tensor-model-parallel-size ${TENSOR_PARALLEL_SIZE} \
  --pipeline-model-parallel-size ${PIPELINE_PARALLEL_SIZE} \
  --sequence-parallel \
  --use-distributed-optimizer \
  --num-layers ${NUM_LAYERS} \
  --hidden-size ${HIDDEN_SIZE} \
  --ffn-hidden-size ${FFN_HIDDEN_SIZE} \
  --num-attention-heads ${NUM_HEADS} \
  --seq-length ${SEQ_LENGTH} \
  --max-position-embeddings ${SEQ_LENGTH} \
  --micro-batch-size ${MICRO_BATCH_SIZE} \
  --global-batch-size ${GLOBAL_BATCH_SIZE} \
  --train-iters ${TRAIN_STEPS} \
  --tokenizer-type Llama2Tokenizer \
  --tokenizer-model ${TOKENIZER_MODEL} \
  --use-checkpoint-args \
  ${CHECKPOINT_ARGS} \
  --save ${CHECKPOINT_SAVE_DIR} \
  --data-path ${DATA_PATH} \
  --split 949,50,1 \
  --distributed-backend nccl \
  --init-method-std 0.02 \
  --lr ${LR} \
  --min-lr ${MIN_LR} \
  --lr-decay-style cosine \
  --weight-decay ${WEIGHT_DECAY} \
  --clip-grad ${GRAD_CLIP} \
  --lr-warmup-iters ${LR_WARMUP_STEPS} \
  --optimizer adam \
  --adam-beta1 0.9 \
  --adam-beta2 0.95 \
  --log-interval 1 \
  --save-interval 500 \
  --eval-interval 100 \
  --eval-iters 10 \
  --bf16 \
  --untie-embeddings-and-output-weights \
  --use-rotary-position-embeddings \
  --normalization RMSNorm \
  --norm-epsilon 1e-5 \
  --no-position-embedding \
  --no-masked-softmax-fusion \
  --attention-dropout 0.0 \
  --hidden-dropout 0.0 \
  --swiglu \
  --use-flash-attn \
  --recompute-activations \
  --recompute-granularity "selective" \
  --use-z-loss \
  --use-mpi \
  --wandb-name ${JOB_NAME} \
  --wandb-project "megatron-lm-3d" \
  --wandb-entity "okoge"
