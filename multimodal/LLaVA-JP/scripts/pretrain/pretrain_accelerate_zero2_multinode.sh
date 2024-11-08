#!/bin/bash

# 引数としてconfig_fileのパスを受け取る
CONFIG_FILE=$1
IMAGE_ENCODER_CONFIG_FILE=$2
DATASET_CONFIG_FILE=$3
MODEL_CONFIG_FILE=$4
OUTPUT_DIR=$5
WANDB_PROJECT=$6
WANDB_NAME=$7


# 引数が指定されていない場合はエラーメッセージを表示して終了
if [ -z "$CONFIG_FILE" ] || [ -z "$IMAGE_ENCODER_CONFIG_FILE" ] || [ -z "$DATASET_CONFIG_FILE" ] || [ -z "$MODEL_CONFIG_FILE" ] || [ -z "$OUTPUT_DIR" ] || [ -z "$WANDB_PROJECT" ] || [ -z "$WANDB_NAME" ]; then
    echo "Invalid argument"
    exit 1
fi

# パスが存在するか確認
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Config file $CONFIG_FILE not found."
    exit 1
fi

if [ ! -f "$IMAGE_ENCODER_CONFIG_FILE" ]; then
    echo "Error: Config file $IMAGE_ENCODER_CONFIG_FILE not found."
    exit 1
fi

if [ ! -f "$DATASET_CONFIG_FILE" ]; then
    echo "Error: Config file $DATASET_CONFIG_FILE not found."
    exit 1
fi

if [ ! -f "$MODEL_CONFIG_FILE" ]; then
    echo "Error: Config file $MODEL_CONFIG_FILE not found."
    exit 1
fi

# 必要なパラメータをjqで読み込んで変数に格納する
VERSION=$(jq -r '.version' $CONFIG_FILE)
FREEZE_BACKBONE=$(jq -r '.freeze_backbone' $CONFIG_FILE)
TUNE_MM_MLP_ADAPTER=$(jq -r '.tune_mm_mlp_adapter' $CONFIG_FILE)
MM_VISION_SELECT_LAYER=$(jq -r '.mm_vision_select_layer' $CONFIG_FILE)
MM_PROJECTOR_TYPE=$(jq -r '.mm_projector_type' $CONFIG_FILE)
MM_VISION_SELECT_FEATURE=$(jq -r '.mm_vision_select_feature' $CONFIG_FILE)
LAZY_PREPROCESS=$(jq -r '.lazy_preprocess' $CONFIG_FILE)
IS_MULTIMODAL=$(jq -r '.is_multimodal' $CONFIG_FILE)
IMAGE_ASPECT_RATIO=$(jq -r '.image_aspect_ratio' $CONFIG_FILE)
OPTIM=$(jq -r '.optim' $CONFIG_FILE)
DOUBLE_QUANT=$(jq -r '.double_quant' $CONFIG_FILE)
QUANT_TYPE=$(jq -r '.quant_type' $CONFIG_FILE)
BITS=$(jq -r '.bits' $CONFIG_FILE)
LORA_ENABLE=$(jq -r '.lora_enable' $CONFIG_FILE)
GROUP_BY_MODALITY_LENGTH=$(jq -r '.group_by_modality_length' $CONFIG_FILE)
FP16=$(jq -r '.fp16' $CONFIG_FILE)
BF16=$(jq -r '.bf16' $CONFIG_FILE)
NUM_TRAIN_EPOCHS=$(jq -r '.num_train_epochs' $CONFIG_FILE)
PER_DEVICE_TRAIN_BATCH_SIZE=$(jq -r '.per_device_train_batch_size' $CONFIG_FILE)
PER_DEVICE_EVAL_BATCH_SIZE=$(jq -r '.per_device_eval_batch_size' $CONFIG_FILE)
GRADIENT_ACCUMULATION_STEPS=$(jq -r '.gradient_accumulation_steps' $CONFIG_FILE)
EVALUATION_STRATEGY=$(jq -r '.evaluation_strategy' $CONFIG_FILE)
SAVE_STRATEGY=$(jq -r '.save_strategy' $CONFIG_FILE)
SAVE_STEPS=$(jq -r '.save_steps' $CONFIG_FILE)
SAVE_TOTAL_LIMIT=$(jq -r '.save_total_limit' $CONFIG_FILE)
LEARNING_RATE=$(jq -r '.learning_rate' $CONFIG_FILE)
WEIGHT_DECAY=$(jq -r '.weight_decay' $CONFIG_FILE)
WARMUP_RATIO=$(jq -r '.warmup_ratio' $CONFIG_FILE)
LOGGING_STEPS=$(jq -r '.logging_steps' $CONFIG_FILE)
GRADIENT_CHECKPOINTING=$(jq -r '.gradient_checkpointing' $CONFIG_FILE)
DATALOADER_NUM_WORKERS=$(jq -r '.dataloader_num_workers' $CONFIG_FILE)
LR_SCHEDULER_TYPE=$(jq -r '.lr_scheduler_type' $CONFIG_FILE)
USE_WANDB=$(jq -r '.use_wandb' $CONFIG_FILE)

VISION_TOWER=$(jq -r '.vision_tower' $IMAGE_ENCODER_CONFIG_FILE)
SCALES=$(jq -r '.scales | @tsv' $IMAGE_ENCODER_CONFIG_FILE)
IMAGE_SIZE=$(jq -r '.image_size' $IMAGE_ENCODER_CONFIG_FILE)

BASE_MODEL=$(jq -r '.base_model' $MODEL_CONFIG_FILE)
MODEL_NAME_OR_PATH=$(jq -r '.model_name_or_path' $MODEL_CONFIG_FILE)
MODEL_MAX_LENGTH=$(jq -r '.model_max_length' $MODEL_CONFIG_FILE)


# シェルスクリプトの実行
accelerate launch --config_file configs/accelerate/pretrain/accelerate_config_zero2_multinode.yaml \
train_llava.py \
    --base_model "$BASE_MODEL" \
    --model_name_or_path "$MODEL_NAME_OR_PATH" \
    --version "$VERSION" \
    --freeze_backbone "$FREEZE_BACKBONE" \
    --tune_mm_mlp_adapter "$TUNE_MM_MLP_ADAPTER" \
    --vision_tower "$VISION_TOWER" \
    --mm_vision_select_layer "$MM_VISION_SELECT_LAYER" \
    --mm_projector_type "$MM_PROJECTOR_TYPE" \
    --mm_vision_select_feature "$MM_VISION_SELECT_FEATURE" \
    --dataset_paths "$DATASET_CONFIG_FILE" \
    --lazy_preprocess "$LAZY_PREPROCESS" \
    --is_multimodal "$IS_MULTIMODAL" \
    --image_aspect_ratio "$IMAGE_ASPECT_RATIO" \
    --optim "$OPTIM" \
    --model_max_length "$MODEL_MAX_LENGTH" \
    --double_quant "$DOUBLE_QUANT" \
    --quant_type "$QUANT_TYPE" \
    --bits "$BITS" \
    --lora_enable "$LORA_ENABLE" \
    --group_by_modality_length "$GROUP_BY_MODALITY_LENGTH" \
    --fp16 "$FP16" \
    --bf16 "$BF16" \
    --output_dir "$OUTPUT_DIR" \
    --num_train_epochs "$NUM_TRAIN_EPOCHS" \
    --per_device_train_batch_size "$PER_DEVICE_TRAIN_BATCH_SIZE" \
    --per_device_eval_batch_size "$PER_DEVICE_EVAL_BATCH_SIZE" \
    --gradient_accumulation_steps "$GRADIENT_ACCUMULATION_STEPS" \
    --evaluation_strategy "$EVALUATION_STRATEGY" \
    --save_strategy "$SAVE_STRATEGY" \
    --save_steps "$SAVE_STEPS" \
    --save_total_limit "$SAVE_TOTAL_LIMIT" \
    --learning_rate "$LEARNING_RATE" \
    --weight_decay "$WEIGHT_DECAY" \
    --warmup_ratio "$WARMUP_RATIO" \
    --logging_steps "$LOGGING_STEPS" \
    --gradient_checkpointing "$GRADIENT_CHECKPOINTING" \
    --dataloader_num_workers "$DATALOADER_NUM_WORKERS" \
    --lr_scheduler_type "$LR_SCHEDULER_TYPE" \
    --use_wandb "$USE_WANDB" \
    --wandb_project "$WANDB_PROJECT" \
    --wandb_name "$WANDB_NAME" \
    --scales $SCALES \
    --image_size $IMAGE_SIZE
