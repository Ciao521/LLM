#!/bin/bash

python train_llava.py \
    --base_model gpt_neox \
    --model_name_or_path rinna/japanese-gpt-neox-small \
    --version plain \
    --freeze_backbone False \
    --tune_mm_mlp_adapter True \
    --vision_tower openai/clip-vit-large-patch14-336 \
    --mm_vision_select_layer -2 \
    --mm_projector_type mlp2x_gelu \
    --mm_vision_select_feature patch \
    --data_path ./dataset/v0/llava_pretrain_stair.json \
    --lazy_preprocess False \
    --is_multimodal True \
    --image_folder ./dataset/v0/images \
    --image_aspect_ratio square \
    --optim adamw_torch \
    --model_max_length 2048 \
    --double_quant True \
    --quant_type nf4 \
    --bits 16 \
    --lora_enable False \
    --group_by_modality_length False \
    --fp16 True \
    --bf16 False \
    --output_dir ./output_llava/checkpoints/pretrain-llava-v1.5-japanese-gpt-neox-small_test \
    --num_train_epochs 1 \
    --per_device_train_batch_size 16 \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 2 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 24000 \
    --save_total_limit 1 \
    --learning_rate 1e-3 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --logging_steps 1 \
    --gradient_checkpointing True \
    --dataloader_num_workers 1 \
    --lr_scheduler_type "cosine" \
    --use_wandb \
    --wandb_project llava-jp-test \
    --wandb_name rinna-gpt_neox_small