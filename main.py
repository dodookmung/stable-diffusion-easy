from module import StableDiffusion as sd




def main():
    PROMPT = "a cat wearing sunglasses, in the style of cyberpunk",
    NEGATIVE_PROMPT = " ",


    # StableDiffusion 인스턴스 생성
    cat = sd(PROMPT, NEGATIVE_PROMPT, seed=42)

    # 이미지 생성
    cat.generate(
        width=512,
        height=512,
        batch_size=1,
        file_name="cool_cat"
    )


if __name__ == "__main__":
    main()