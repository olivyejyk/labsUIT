import unittesе
from unittest.mock import Mock, patch, MagicMock
from tkinter import Tk
from PIL import Image
from main import SlideModel, SlideView, SlideController

class TestSlideModel(unittest.TestCase):
    def setUp(self):
        self.image_paths = ["image1.jpg", "image2.jpg", "image3.jpg"]
        self.model = SlideModel(self.image_paths)

    def test_initial_image(self):
        self.assertEqual(self.model.get_current_image_path(), "image1.jpg")

    def test_next_slide(self):
        self.model.next_slide()
        self.assertEqual(self.model.get_current_image_path(), "image2.jpg")

    def test_cycle_slides(self):
        for _ in range(3):
            self.model.next_slide()
        self.assertEqual(self.model.get_current_image_path(), "image1.jpg")

class TestSlideView(unittest.TestCase):
    @patch("main.ImageTk.PhotoImage")
    @patch("main.Image.open")
    @patch("main.Canvas.create_image")
    @patch("main.Canvas")
    def test_display_image(self, mock_canvas, mock_create_image, mock_open, mock_photoimage):
        from tkinter import Tk
        root = Tk()
        root.withdraw()  # Ховаємо головне вікно

        # Моки для Canvas
        mock_canvas_instance = mock_canvas.return_value

        # Мок для зображення
        mock_image = Mock()
        mock_image.size = (800, 600)
        mock_image.mode = "RGB"
        mock_image.resize.return_value = mock_image
        mock_open.return_value = mock_image

        # Мок для PhotoImage
        mock_photo = Mock()
        mock_photoimage.return_value = mock_photo

        view = SlideView(root, Mock())  # Створення SlideView

        # Виклик display_image
        view.display_image("image1.jpg")

        # Перевірка викликів
        mock_open.assert_called_once_with("image1.jpg")
        mock_image.resize.assert_called_once_with((800, 600), Image.Resampling.LANCZOS)
        mock_photoimage.assert_called_once_with(mock_image)
        mock_canvas_instance.create_image.assert_called_once_with(400, 300, image=mock_photo)

        root.destroy()  # Закриваємо Tk

    @patch("main.Tk")
    def test_set_on_click_handler(self, MockTk):
        mock_root = MockTk()
        mock_controller = Mock()
        view = SlideView(mock_root, mock_controller)
        view.canvas = MagicMock()
        view.canvas.bind = Mock()

        mock_handler = Mock()
        view.set_on_click_handler(mock_handler)

        view.canvas.bind.assert_called_once_with("<Button-1>", mock_handler)

class TestSlideController(unittest.TestCase):
    @patch("main.Tk")
    def setUp(self, MockTk):
        self.image_paths = ["image1.jpg", "image2.jpg"]
        self.model = SlideModel(self.image_paths)
        self.mock_root = MockTk()
        self.view = SlideView(self.mock_root, None)
        self.controller = SlideController(self.model, self.view)
        self.view.display_image = Mock()

    def test_handle_click(self):
        self.controller.handle_click(Mock())
        self.assertEqual(self.model.current_index, 1)
        self.view.display_image.assert_called_once_with("image2.jpg")

    def test_update_view(self):
        self.controller.update_view()
        self.view.display_image.assert_called_once_with("image1.jpg")

if __name__ == "__main__":
    unittest.main()
