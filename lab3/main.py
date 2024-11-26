from tkinter import Tk, Canvas, filedialog
from PIL import Image, ImageTk

# Model: Управління даними (шлях до зображень і поточний індс)
class SlideModel:
    def __init__(self, image_paths):
        self.image_paths = image_paths
        self.current_index = 0

    def get_current_image_path(self):
        return self.image_paths[self.current_index]

    def next_slide(self):
        self.current_index = (self.current_index + 1) % len(self.image_paths)

# View: Відображення графічного інтерфейсу
class SlideView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.canvas = Canvas(root, width=800, height=600, bg="black")
        self.canvas.pack()

    def display_image(self, image_path):
        # Завантаження зображення через Pillow
        image = Image.open(image_path)
        image = image.resize((800, 600), Image.Resampling.LANCZOS)  # Масштабування зображення
        tk_image = ImageTk.PhotoImage(image)

        # Збереження посилання на зображення
        self.canvas.image = tk_image  # Зберігаємо посилання для уникнення очищення пам'яті
        self.canvas.create_image(400, 300, image=tk_image)

    def set_on_click_handler(self, handler):
        self.canvas.bind("<Button-1>", handler)

# Controller: Логіка зв'язку між Model і View
class SlideController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_on_click_handler(self.handle_click)

    def handle_click(self, event):
        self.model.next_slide()
        self.update_view()

    def update_view(self):
        image_path = self.model.get_current_image_path()
        self.view.display_image(image_path)

# Головна функція
def main():
    # Вибір зображень через діалогове вікно
    image_paths = filedialog.askopenfilenames(
        title="Виберіть зображення",
        filetypes=[("Зображення", "*.bmp *.jpeg *.jpg *.png")]
    )
    if not image_paths:
        print("Не вибрано зображень.")
        return

    root = Tk()
    root.title("Слайд-шоу")

    # Ініціалізація компонентів MVC
    model = SlideModel(image_paths)
    view = SlideView(root, None)
    controller = SlideController(model, view)

    # Показ першого зображення
    controller.update_view()

    root.mainloop()

if __name__ == "__main__":
    main()
