import flet as ft

class SelectorColor(ft.Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expand = True

        self.slides = {f'{l}_slider{i}': ft.Slider(min=0, max=255, value=0,height=30,  active_color="#00ADFF",thumb_color ="#00ADFF",on_change=self.update_color, data = i) for i in range(1, 10) for l in ['r', 'g', 'b']}
        self.slides['r_slider1'].value = 255
        self.slides['b_slider2'].value = 255
        self.slides['b_slider5'].value = 100
        self.slides['r_slider3'].value = 255
        self.slides['g_slider3'].value = 255
        self.slides['b_slider3'].value = 255

        # self.cor_primaria = ft.Text("Cor Primária", size = 20, weight= 'BOLD', data = 'black')
        # self.cor_fundo = ft.Text("Cor do Fundo", size = 20, weight= 'BOLD', data = 'black')
        # self.cor_texto = ft.Text("Cor do Texto", size = 20, weight= 'BOLD', data = 'black')
        # self.cor_combras = ft.Text("Cor das Sombras", size = 20, weight= 'BOLD', data = 'black')
        # self.cor_gradiente = ft.Text("Cor do Gradiente", size = 20, weight= 'BOLD', data = 'black')
        # self.cor_gradiente = ft.Text("Cor do Título", size = 20, weight= 'BOLD', data = 'black')
        listatitulos = ["Cor Primária", "Cor do Fundo", "Cor do Texto","Cor das Sombras", 
                        "Cor do Gradiente","Cor do Título", "Cor do Texto 1", "Cor do Texto 2",
                        "Cor das Bordas", 
        
        
        ]
        self.cores = {i: ft.Text(i, size = 20, weight= 'BOLD', data = 'black') for i in listatitulos}

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
            # shadow=ft.BoxShadow(
            #     spread_radius=0,
            #     blur_radius=10,
            #     color="#000000"
            # )
           
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
            # gradient=ft.LinearGradient(
            #     begin=ft.alignment.top_center,
            #     end=ft.alignment.bottom_center,
            #     colors=['#0000ff', "#0000ff"]
            # )
            )
        self.ativar_sombras = ft.Checkbox(label="Ativar Sombras", value =False, on_change=self.GerenciarSombras)
        self.ativar_gradiente = ft.Checkbox(label="Ativar Gradiente", value =False, on_change=self.GerenciarGradiente)
        self.ativar_bordas = ft.Checkbox(label="Ativar Bordas", value =False, on_change=self.GerenciarBordas)

        self.sombras = self.GerarColunaCores("Cor das Sombras", 4)
        self.gradiente = self.GerarColunaCores("Cor do Gradiente", 5)
        self.bordas = self.GerarColunaCores( "Cor das Bordas", 9)
        self.sombras.visible = False
        self.gradiente.visible = False
        self.bordas.visible = False


        col_A = ft.Column(
            [
                self.color_box2,
                ft.Row([self.ativar_sombras], alignment='center', spacing=1,wrap=True),
                self.GerarColunaCores("Cor Primária", 1),                         
                self.GerarColunaCores("Cor do Fundo", 2),
            ],
            width=310,
            alignment='start',
            horizontal_alignment='center',
        )
        col_B = ft.Column(
            [
                ft.Divider(20,color='transparent'),
                self.ativar_gradiente,
                self.GerarColunaCores("Cor do Texto", 3),                         
                self.GerarColunaCores("Cor do Título", 6),                         
                self.GerarColunaCores("Cor do Texto 1", 7), 
            ],
            width=310,
            alignment='start',
            horizontal_alignment='center',
        )
        col_C = ft.Column(
            [
                ft.Divider(20,color='transparent'),
                self.ativar_bordas,
                self.GerarColunaCores("Cor do Texto 2", 8),                         
                self.bordas,                         
                self.sombras, 
            ],
            width=310,
            alignment='start',
            horizontal_alignment='center',
        )

        col_D = ft.Column(
            [
                ft.Divider(60,color='transparent'),
                self.gradiente,
                 
                
            ],
            width=310,
            alignment='start',
            horizontal_alignment='center',
        )        
        self.content = ft.Row(
            controls = [                                                      
                col_A,
                col_B,
                col_C,                                            
                col_D,                                            
            ], 
            wrap=True,
            spacing=20,
            run_spacing=10,
            alignment='center',
            vertical_alignment='start',
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
                colors=[self.cores["Cor do Fundo"].data, self.cores["Cor do Gradiente"].data]
            )
        else:
            self.color_box2.gradient = None
        self.gradiente.visible = self.ativar_gradiente.value
        self.color_box2.update()
        self.update()

    def GerenciarBordas(self, e):
        if self.ativar_bordas.value:
            self.color_box.border = ft.border.all(1, "#000000")

        else:
            self.color_box.border = None
        self.bordas.visible = self.ativar_bordas.value
        self.color_box.update()
        self.update()

    def GerarColunaCores(self, nomepropriedade, index):
        return ft.Container(
            content = ft.Column(
                [
                    ft.Row(
                            [
                            self.cores[nomepropriedade],
                            ft.IconButton(
                                icon=ft.Icons.COPY, 
                                icon_size = 10,                                       
                                splash_radius=0,
                                on_click=lambda e: e.page.set_clipboard(f'"{self.cores[nomepropriedade].data}"')
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
            border=ft.border.all(1, 'grey800'),
            border_radius=15,
            padding=20,
        )
    

    def update_color(self, e):
        if e.control.data == 1:                
            color = f'#{int(self.slides['r_slider1'].value):02X}{int(self.slides['g_slider1'].value):02X}{int(self.slides['b_slider1'].value):02X}'
            self.color_box.bgcolor = color
            self.SetValues('Cor Primária', color)

        elif e.control.data == 2 and not self.ativar_gradiente.value:
            color = f'#{int(self.slides['r_slider2'].value):02X}{int(self.slides['g_slider2'].value):02X}{int(self.slides['b_slider2'].value):02X}'
            self.color_box2.bgcolor = color
            self.SetValues("Cor do Fundo", color)

        elif e.control.data == 2 and  self.ativar_gradiente.value:
            color = f'#{int(self.slides['r_slider2'].value):02X}{int(self.slides['g_slider2'].value):02X}{int(self.slides['b_slider2'].value):02X}'
            self.color_box2.gradient.colors[0] = color         
            self.SetValues("Cor do Gradiente", color)

        elif e.control.data == 3:
            color = f'#{int(self.slides['r_slider3'].value):02X}{int(self.slides['g_slider3'].value):02X}{int(self.slides['b_slider3'].value):02X}'
            self.color_text.color = color
            self.SetValues("Cor do Texto", color)

        elif e.control.data == 4 and self.ativar_sombras.value:
            color = f'#{int(self.slides['r_slider4'].value):02X}{int(self.slides['g_slider4'].value):02X}{int(self.slides['b_slider4'].value):02X}'
            self.color_box.shadow.color=color
            self.SetValues("Cor das Sombras", color)

        elif e.control.data == 5 and self.ativar_gradiente.value:
            color = f'#{int(self.slides['r_slider5'].value):02X}{int(self.slides['g_slider5'].value):02X}{int(self.slides['b_slider5'].value):02X}'
            self.color_box2.gradient.colors[1] = color
            self.SetValues("Cor do Gradiente", color)

        elif e.control.data == 6:
            color = f'#{int(self.slides['r_slider6'].value):02X}{int(self.slides['g_slider6'].value):02X}{int(self.slides['b_slider6'].value):02X}'
            self.titulo.color=color
            self.SetValues("Cor do Título", color)

        elif e.control.data == 7:
            color = f'#{int(self.slides['r_slider7'].value):02X}{int(self.slides['g_slider7'].value):02X}{int(self.slides['b_slider7'].value):02X}'
            self.texto1.color=color
            self.SetValues("Cor do Texto 1", color)

        elif e.control.data == 8:
            color = f'#{int(self.slides['r_slider8'].value):02X}{int(self.slides['g_slider8'].value):02X}{int(self.slides['b_slider8'].value):02X}'
            self.texto2.color=color
            self.SetValues("Cor do Texto 2", color)


        elif e.control.data == 9:
            color = f'#{int(self.slides['r_slider9'].value):02X}{int(self.slides['g_slider9'].value):02X}{int(self.slides['b_slider9'].value):02X}'
            self.color_box.border =  ft.border.all(1, color)
            self.SetValues("Cor das Bordas", color)

        self.update()


    def SetValues(self, nome, color):
        self.cores[nome].value = f'{nome} ({color})'
        self.cores[nome].data = color

    # def did_mount(self):
    #     if not self.page.theme:
    #         self.page.theme = ft.Theme()
            
    #     self.page.theme.slider_theme = ft.SliderTheme(
    #         active_track_color="#0000FB",
    #         thumb_color ="#0000FB",
    #     )
    #     self.page.update()


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
