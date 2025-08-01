import asyncio
from tkinter import ttk, messagebox as mb, Tk, Label, Entry, Button, Toplevel, Frame
from g4f.client import AsyncClient
from PIL import Image, ImageTk
import io
import requests


async def main(prompt_text):
    client = AsyncClient()
    response = await client.images.generate(
        prompt=prompt_text,
        model="flux",
        response_format="url"
    )
    return response.data[0].url


def prog():
    prompt_text = entry.get()
    if not prompt_text.strip():
        mb.showwarning('Пустой ввод', 'Введите запрос')
        return
    global saved_prompt
    saved_prompt = prompt_text
    progress['value'] = 0
    progress.start(30)
    window.after(3000, show_image)


def show_image():
    try:
        image_url = asyncio.run(main(saved_prompt))
        if image_url:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            image = Image.open(io.BytesIO(response.content))
            image.thumbnail((350, 350))
            tk_image = ImageTk.PhotoImage(image)
            tab = ttk.Frame(notebook)
            idx = notebook.index('end') + 1
            notebook.add(tab, text=f'Изображение {idx}')

            label = ttk.Label(tab, image=tk_image)
            label.image = tk_image
            label.pack(padx=10, pady=10)
    except Exception as e:
        mb.showerror('Ошибка', f'Ошибка при генерации: {e}')
    finally:
        progress.stop()


def clean():
    for tab in notebook.tabs():
        notebook.forget(tab)


window = Tk()
window.title('Сгенерировать изображение')
window.geometry('350x150')

label = Label(text='Введите свой запрос и нажмите на кнопку')
label.pack(pady=5)

entry = ttk.Entry(window, width=40)
entry.pack(pady=5)


frames = Frame(window)
frames.pack()
button = ttk.Button(frames, text='Сгенерировать', command=prog)
button.pack(side='left', pady=10, padx=5)
clean_button = ttk.Button(frames, text='Очистить вкладки', command=clean)
clean_button.pack(side='left', pady=10, padx=5)

progress = ttk.Progressbar(mode='determinate', length=300)
progress.pack(pady=10)


top_level_window = Toplevel(window)
top_level_window.title('Сгенерированные изображения')

notebook = ttk.Notebook(top_level_window)
notebook.pack(expand=True, fill='both', padx=10, pady=10)

saved_prompt = ''
window.mainloop()