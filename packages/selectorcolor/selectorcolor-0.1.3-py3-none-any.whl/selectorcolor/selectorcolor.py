import flet as ft

class SelectorColor(ft.Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expand = True

        self.slides = {
            l: ft.Slider(
                min=0, 
                max=255, 
                value=0,
                height=30,  
                active_color="#00ADFF",
                thumb_color ="#00ADFF",
                on_change=self.update_color,                 
            ) 
            for l in ['r', 'g', 'b']
        }

 

        self.titulo = ft.Text(
            value="Título", 
            selectable=True,
            size = 20, 
            weight= 'BOLD', 
            color = '#ffffff'
        )
        self.texto1 = ft.Text(
            value="Texto 1", 
            selectable=True,
            size = 15, 
            # weight= 'BOLD', 
            color = '#ffffff'
        )
        self.texto2 = ft.Text(
            value="Texto 2", 
            selectable=True,
            size = 12, 
          
            color = '#ffffff'
        )                
        self.color_text = ft.Text(
            value="Texto", 
            selectable=True,
            size = 20, 
            weight= 'BOLD', 
            color = '#ffffff'
        )
        self.color_box = ft.Container(
            content = self.color_text, 
            width=100, 
            height=100, 
            bgcolor="#ff0000", 
            border_radius=12,
            alignment=ft.alignment.center,
           
        )
        self.color_box2 = ft.Container(
            content=ft.Column(
                controls = [
                    self.titulo,
                    self.color_box,
                    self.texto1,
                    self.texto2
                ],
                horizontal_alignment='center',
                tight=True,
                spacing= 3,
            ),
            alignment=ft.alignment.center,
            width=200, 
            height=200, 
            border_radius=12,
            bgcolor="#0000ff",

            )
        
        # self.ativar_sombras = ft.Checkbox(label="Ativar Sombras", value =False, on_change=self.GerenciarSombras)
        self.ativar_gradiente = ft.Checkbox(label="Ativar Gradiente", value =False, on_change=self.GerenciarGradiente)
        self.ativar_bordas = ft.Checkbox(label="Ativar Bordas", value =False, on_change=self.GerenciarBordas)



        self.datas = {
            "Container": lambda color: setattr(self.color_box, 'bgcolor', color), 
            "Fundo": lambda color: setattr(self.color_box2, 'bgcolor', color),
            "Texto": lambda color: setattr(self.color_text, 'color', color),
            "Título": lambda color: setattr(self.titulo, 'color', color),
            "Texto 1": lambda color: setattr(self.texto1, 'color', color),
            "Texto 2": lambda color: setattr(self.texto2, 'color', color),
            "Bordas": lambda color: setattr(self.color_box, 'border', ft.border.all(1, color)),
            "Sombras": lambda color: setattr(self.color_box, 'shadow', ft.BoxShadow(spread_radius=0, blur_radius=20, color=color)),
            "Gradiente": lambda color: setattr(self.color_box2, 'gradient', ft.LinearGradient(begin=ft.alignment.top_center, end=ft.alignment.bottom_center, colors=[self.color_box2.bgcolor, color])),         
        }



        self.objetos = ft.Dropdown(
            width=250,
            options=[ft.dropdown.Option(i) for i in self.datas.keys()],
            hint_text="Selecione o objeto",
            filled=True,
            border_radius=15,
            on_change=self.SetObjeto,
        )

        self.cor = 'black'

      
        self.content = ft.Row(
            controls = [                                                      
                self.color_box2,
                # ft.Row([self.ativar_sombras], alignment='center', spacing=1,wrap=True),
                ft.Container(
                    content = ft.Column(
                        [
                            ft.Row(
                                    [
                                   self.objetos,
                                    ft.IconButton(
                                        icon=ft.Icons.COPY, 
                                        icon_size = 10,                                       
                                        splash_radius=0,
                                        on_click=lambda e: e.page.set_clipboard(f'"{self.cor}"')
                                    )
                                ], 
                                spacing = 0,
                                wrap=False,                                       
                            ),                                    
                            ft.Row([ft.Text("Vermelho", selectable=True, width=70),self.slides[f'r'],], spacing=0),
                            ft.Row([ft.Text("Verde", selectable=True, width=70),self.slides[f'g'],], spacing=0),
                            ft.Row([ft.Text("Azul", selectable=True, width=70),self.slides[f'b'],], spacing=0),
                        ],
                        width=300,
                        spacing=0,
                        run_spacing=0,
                    ),
                    border=ft.border.all(1, 'grey800'),
                    border_radius=15,
                    padding=20,
                )                                                           
            ], 
            wrap=True,
            spacing=20,
            run_spacing=10,
            alignment='center',
            vertical_alignment='start',
        )




    def SetObjeto(self, e):
        self.slides['r'].data = e.control.value
        self.slides['g'].data = e.control.value
        self.slides['b'].data = e.control.value

    def GerenciarSombras(self, e):
        if self.ativar_sombras.value:
            self.color_box.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color="#000000"
            )
        else:
            self.color_box.shadow = None
        # self.sombras.visible = self.ativar_sombras.value
        self.color_box.update()
        self.update()

    def GerenciarGradiente(self, e):
        if self.ativar_gradiente.value:
            self.color_box2.gradient = ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[self.cores["Cor do Fundo"].data, self.cores["Cor do Gradiente"].data]
            )
        else:
            self.color_box2.gradient = None
        # self.gradiente.visible = self.ativar_gradiente.value
        self.color_box2.update()
        self.update()

    def GerenciarBordas(self, e):
        if self.ativar_bordas.value:
            self.color_box.border = ft.border.all(1, "#000000")

        else:
            self.color_box.border = None
        # self.bordas.visible = self.ativar_bordas.value
        self.color_box.update()
        self.update()

    def update_color(self, e):
        self.cor = f'#{int(self.slides['r'].value):02X}{int(self.slides['g'].value):02X}{int(self.slides['b'].value):02X}'
        self.datas[e.control.data](self.cor)
        self.update()
        self.page.client_storage.set(f'{self.page.title}_{e.control.data}', self.cor)

    def GetColorSafe(self, key):
        return self.page.client_storage.get(f'{self.page.title}_{key}')

    def did_mount(self):
        self.titulo.color = self.GetColorSafe('Título')
        self.texto1.color = self.GetColorSafe('Texto 1')
        self.texto2.color = self.GetColorSafe('Texto 2')         
        self.color_text.color = self.GetColorSafe('Texto')
        self.color_box.bgcolor = self.GetColorSafe('Container')
        self.color_box2.bgcolor = self.GetColorSafe('Fundo')
        
        self.page.update()

def main(page):
    page.title = "Seletor de Cores"
    page.window.width = 1380
    page.window.height = 700

    page.add(
        SelectorColor()
    )
def Iniciar():
    ft.app(target=main)
if __name__ == "__main__":  
    ft.app(target=main)
