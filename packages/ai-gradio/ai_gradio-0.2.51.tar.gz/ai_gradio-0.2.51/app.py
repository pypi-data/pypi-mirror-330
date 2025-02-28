import gradio as gr
import ai_gradio


gr.load(
    name='openrouter:openai/gpt-4.5-preview',
    src=ai_gradio.registry,
    coder=True,
).launch()
