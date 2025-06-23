import torch
import random
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler



class StableDiffusion:
    def __init__(self, prompt="a cat", negative_prompt=" ", seed=42, checkpoint="runwayml/stable-diffusion-v1-5"):
        # 디바이스 설정
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f'torch device : {self.device}')
        # 시드 고정
        seed = int(seed)
        torch.manual_seed(seed)
        random.seed(seed)
        self.prompt = prompt
        self.negative_prompt = negative_prompt

        # 모델 로드
        self.checkpoint = checkpoint
        print(f'스테이블 디퓨전 checkpoint : {self.checkpoint}')
        self.pipe = StableDiffusionPipeline.from_pretrained(
            self.checkpoint,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        ).to(self.device)
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)
        self.pipe.enable_attention_slicing()
        # xformers 미설치 시 예외를 무시하고 계속 실행
        try:
            self.pipe.enable_xformers_memory_efficient_attention()
        except ModuleNotFoundError:
            print("[WARN] xformers 미설치: memory-efficient attention 활성화 스킵")
        
    def generate(self, batch_size=4, width=512, height=512, num_inference_steps=30, file_name="sample"):
        # 프롬프트가 리스트가 아니라 문자열임을 보장
        prompt = str(self.prompt) if not isinstance(self.prompt, str) else self.prompt
        negative_prompt = str(self.negative_prompt) if not isinstance(self.negative_prompt, str) else self.negative_prompt

        print(f"사용 프롬프트:\n{prompt}\n")
        print(f"네거티브 프롬프트:\n{negative_prompt}\n")
        # 이미지 생성
        images = self.pipe(
            prompt=[prompt] * batch_size,  # 동일한 프롬프트 반복
            negative_prompt=[negative_prompt] * batch_size,
            width=int(width),
            height=int(height),
            num_inference_steps=int(num_inference_steps),
            guidance_scale=7.5
        ).images

        # 이미지 저장
        for i, img in enumerate(images):
            output_path = f"{file_name}_{i+1}.png"
            img.save(output_path)
            print(f"이미지 저장 완료: {output_path}")