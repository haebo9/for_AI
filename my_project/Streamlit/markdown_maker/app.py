import streamlit as st
from model import convert_to_markdown

PASSWORD = "9999"  # 원하는 4자리 비밀번호로 설정

def main():
    st.set_page_config(
        page_title="Text to Markdown Converter",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    st.title("Text to Markdown Converter")
    st.write("입력한 일반 텍스트를 깔끔한 마크다운(README용)으로 변환해줍니다.")

    # 세션 상태에서 인증 여부 확인
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    # 인증되지 않은 경우: 비밀번호 입력 UI만 노출
    if not st.session_state.authenticated:
        password = st.text_input("4자리 비밀번호를 입력하세요.", type="password", max_chars=4)
        if st.button("로그인", disabled=not (password and len(password) == 4 and password.isdigit())):
            if password == PASSWORD:
                st.session_state.authenticated = True
                st.success("로그인 성공! 변환 기능을 사용할 수 있습니다.")
                st.rerun()
            else:
                st.error("비밀번호가 올바르지 않습니다.")
        st.stop()

    # 인증된 경우: 변환 기능 UI 노출
    # 변환 엔진 선택
    provider = st.selectbox(
        "변환 엔진을 선택하세요.",
        options=["openai", "gemini"],
        format_func=lambda x: "OpenAI" if x == "openai" else "Gemini"
    )

    # 텍스트 입력란
    user_input = st.text_area(
        "여기에 변환할 텍스트를 입력하세요.",
        placeholder="예시: 이곳에 변환할 텍스트를 입력하세요.",
        height=300
    )

    if st.button("마크다운으로 변환", disabled=not user_input):
        with st.spinner('마크다운으로 변환 중...'):
            markdown_text = convert_to_markdown(user_input, provider=provider)
        # 변환된 마크다운을 세션에 저장
        st.session_state.markdown_text = markdown_text

    # 세션에 마크다운이 있으면 탭 표시
    if "markdown_text" in st.session_state:
        tab1, tab2 = st.tabs(["마크다운 코드", "미리보기"])
        with tab1:
            # text_area로 수정 가능하게
            edited_markdown = st.text_area(
                "마크다운 코드를 자유롭게 수정하세요.",
                value=st.session_state.markdown_text,
                height=300,
                key="markdown_editor"
            )
            # 수정 내용 세션에 반영
            st.session_state.markdown_text = edited_markdown
        with tab2:
            preview_md = edited_markdown.replace("```markdown", "").replace("```", "")
            st.markdown(preview_md, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("제작자: [haebo9 github](https://github.com/haebo9/for_AI)")

if __name__ == "__main__":
    main()