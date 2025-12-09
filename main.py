import flet as ft
from services.weather_service import WeatherService
from components.weather_card import WeatherCard
from components.search_bar import SearchBar
from config.settings import APP_TITLE, DEFAULT_CITY


class WeatherApp(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        self.page = page
        self.weather_service = WeatherService()
        self.weather_card = WeatherCard()

        self.setup_page()
        self.build_ui()

        # Cargar clima por defecto
        self.search_weather(DEFAULT_CITY)

    def setup_page(self):
        """Configura la página principal"""
        self.page.title = APP_TITLE
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.scroll = ft.ScrollMode.ADAPTIVE

    def build_ui(self):
        """Construye la interfaz de usuario"""
        # Título
        title = ft.Text(
            APP_TITLE,
            size=32,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )

        # Barra de búsqueda
        search_bar = SearchBar(on_search=self.search_weather)

        # Indicador de carga
        self.loading = ft.ProgressRing(visible=False)

        # Mensaje de error
        self.error_message = ft.Text(
            "",
            color=ft.Colors.RED,
            text_align=ft.TextAlign.CENTER,
            visible=False
        )

        # Añadir al layout principal (esta clase es un Column)
        self.controls = [
            title,
            ft.Divider(),
            search_bar,
            ft.Container(
                content=self.loading,
                alignment=ft.alignment.center,
                height=50
            ),
            self.error_message,
            self.weather_card
        ]

        self.page.add(self)

    def search_weather(self, city_name):
        """Busca el clima de una ciudad"""
        self.show_loading(True)
        self.hide_error()

        weather_data = self.weather_service.get_weather(city_name)

        if weather_data:
            self.weather_card.update_weather(weather_data)
        else:
            self.show_error(f"No se pudo obtener el clima de '{city_name}'.")

        self.show_loading(False)

    def show_loading(self, show):
        self.loading.visible = show
        self.page.update()

    def show_error(self, message):
        self.error_message.value = message
        self.error_message.visible = True
        self.page.update()

    def hide_error(self):
        self.error_message.visible = False
        self.page.update()


def main(page: ft.Page):
    WeatherApp(page)


if __name__ == "__main__":
    ft.app(target=main)
