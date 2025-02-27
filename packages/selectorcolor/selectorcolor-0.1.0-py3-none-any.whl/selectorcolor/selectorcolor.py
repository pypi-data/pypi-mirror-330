import flet as ft

class SelectorColor(ft.Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expand = True

        self.slides = {f'{l}_slider{i}': ft.Slider(min=0, max=255, value=0, on_change=self.update_color, data = i) for i in range(1, 6) for l in ['r', 'g', 'b']}
        self.slides['r_slider1'].value = 255
        self.slides['b_slider2'].value = 255
        self.slides['b_slider5'].value = 100
        self.slides['r_slider3'].value = 255
        self.slides['g_slider3'].value = 255
        self.slides['b_slider3'].value = 255

        self.cor_primaria = ft.Text("Cor Primária", size = 20, weight= 'BOLD', data = 'black')
        self.cor_fundo = ft.Text("Cor do Fundo", size = 20, weight= 'BOLD', data = 'black')
        self.cor_texto = ft.Text("Cor do Texto", size = 20, weight= 'BOLD', data = 'black')
        self.cor_combras = ft.Text("Cor das Sombras", size = 20, weight= 'BOLD', data = 'black')
        self.cor_gradiente = ft.Text("Cor das Gradiente", size = 20, weight= 'BOLD', data = 'black')

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
            alignment=ft.alignment.center,
            # shadow=ft.BoxShadow(
            #     spread_radius=0,
            #     blur_radius=10,
            #     color="#000000"
            # )
           
        )
        self.color_box2 = ft.Container(
            content=self.color_box,
            alignment=ft.alignment.center,
            width=200, 
            height=200, 
            bgcolor="#0000ff",
            # gradient=ft.LinearGradient(
            #     begin=ft.alignment.top_center,
            #     end=ft.alignment.bottom_center,
            #     colors=['#0000ff', "#0000ff"]
            # )
            )
        self.ativar_sombras = ft.Checkbox(label="Ativar Sombras", value =False, on_change=self.GerenciarSombras)
        self.ativar_gradiente = ft.Checkbox(label="Ativar Gradiente", value =False, on_change=self.GerenciarGradiente)

        self.sombras = self.GerarColunaCores(self.cor_combras, 4)
        self.gradiente = self.GerarColunaCores(self.cor_gradiente, 5)
        self.sombras.visible = False
        self.gradiente.visible = False
        self.content = ft.Column(
            [
                self.color_box2,                
                ft.Row([self.ativar_sombras,self.ativar_gradiente], alignment='center'),
                ft.Row(
                    controls = [                                                      
                            self.GerarColunaCores(self.cor_primaria, 1),                         
                            self.GerarColunaCores(self.cor_fundo, 2),                         
                            self.GerarColunaCores(self.cor_texto, 3),                         
                            self.sombras, 
                            self.gradiente, 
                                                    
                    ], 
                    wrap=True,
                    spacing=20,
                    run_spacing=10,
                    alignment='center',
                ),
            ],
            horizontal_alignment='center',
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
        )
        

    def GerenciarSombras(self, e):
        if self.ativar_sombras.value:
            self.color_box.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color="#000000"
            )
        else:
            self.color_box.shadow = None
        self.sombras.visible = self.ativar_sombras.value
        self.color_box.update()
        self.update()

    def GerenciarGradiente(self, e):
        if self.ativar_gradiente.value:
            self.color_box2.gradient = ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=['#0000ff', "#0000ff"]
            )
        else:
            self.color_box2.gradient = None
        self.gradiente.visible = self.ativar_gradiente.value
        self.color_box2.update()
        self.update()

    def GerarColunaCores(self, propriedade, index):
        return ft.Container(
            content = ft.Column(
                [
                    ft.Row(
                            [
                            propriedade,
                            ft.IconButton(
                                icon=ft.Icons.COPY, 
                                icon_size = 10,                                       
                                splash_radius=0,
                                on_click=lambda e: e.page.set_clipboard(f'{propriedade.data}')
                            )
                        ], 
                        spacing = 0,
                        wrap=False,                                       
                    ),                                    
                    ft.Row([ft.Text("Vermelho", selectable=True, width=70),self.slides[f'r_slider{index}'],], spacing=0),
                    ft.Row([ft.Text("Verde", selectable=True, width=70),self.slides[f'g_slider{index}'],], spacing=0),
                    ft.Row([ft.Text("Azul", selectable=True, width=70),self.slides[f'b_slider{index}'],], spacing=0),
                ],
                width=300,
                spacing=0,
                run_spacing=0,
            ),
            border=ft.border.all(1, ft.colors.GREY_800),
            border_radius=15,
            padding=20,
        )
    

    def update_color(self, e):
        if e.control.data == 1:                
            color = f'#{int(self.slides['r_slider1'].value):02X}{int(self.slides['g_slider1'].value):02X}{int(self.slides['b_slider1'].value):02X}'
            self.color_box.bgcolor = color
            self.cor_primaria.value = f'Cor Primária ({color})'
            self.cor_primaria.data = color

        elif e.control.data == 2 and not self.ativar_gradiente.value:
            color = f'#{int(self.slides['r_slider2'].value):02X}{int(self.slides['g_slider2'].value):02X}{int(self.slides['b_slider2'].value):02X}'
            self.color_box2.bgcolor = color
            self.cor_fundo.value = f'Cor do Fundo ({color})'
            self.cor_fundo.data = color

        elif e.control.data == 2 and  self.ativar_gradiente.value:
            color = f'#{int(self.slides['r_slider2'].value):02X}{int(self.slides['g_slider2'].value):02X}{int(self.slides['b_slider2'].value):02X}'
            self.color_box2.gradient.colors[0] = color
            self.cor_gradiente.value = f'Cor do Gradiente ({color})'
            self.cor_gradiente.data = color           

        elif e.control.data == 3:
            color = f'#{int(self.slides['r_slider3'].value):02X}{int(self.slides['g_slider3'].value):02X}{int(self.slides['b_slider3'].value):02X}'
            self.color_text.color = color
            self.cor_texto.value = f'Cor do Texto ({color})'
            self.cor_texto.data = color

        elif e.control.data == 4 and self.ativar_sombras.value:
            color = f'#{int(self.slides['r_slider4'].value):02X}{int(self.slides['g_slider4'].value):02X}{int(self.slides['b_slider4'].value):02X}'
            self.color_box.shadow.color=color
            self.cor_combras.value = f'Cor das Sombras ({color})'
            self.cor_combras.data = color

        elif e.control.data == 5 and self.ativar_gradiente.value:
            color = f'#{int(self.slides['r_slider5'].value):02X}{int(self.slides['g_slider5'].value):02X}{int(self.slides['b_slider5'].value):02X}'
            self.color_box2.gradient.colors[1] = color
            self.cor_gradiente.value = f'Cor do Gradiente ({color})'
            self.cor_gradiente.data = color

        self.update()


def main(page):
    page.title = "Seletor de Cores"
    page.window.width = 1500

    page.add(
        SelectorColor()
    )
def Iniciar():
    ft.app(target=main)
if __name__ == "__main__":  
    ft.app(target=main)
