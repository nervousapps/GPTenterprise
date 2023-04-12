from auto_generated_website.generate_html import generate_html_article

def test_generate_html_article():
    article_prompt = "Write an article about the benefits of meditation."
    generated_html_article = generate_html_article(article_prompt)
    print(generated_html_article)
    assert generated_html_article