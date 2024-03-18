import flet as ft
import aiohttp
import asyncio

current_pokemon = 0

async def main(page: ft.Page):
    page.window_width = 720
    page.window_height = 1280
    page.window_resizable = False
    page.padding = 0
    page.fonts = {
        "zpix": "https://github.com/SolidZORO/zpix-pixel-font/releases/download/v3.1.9/zpix.ttf",
    }

    page.theme = ft.Theme(font_family="zpix")
    
    
    async def request (url):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(url) as response:
                return await response.json()
            
    async def event(e: ft.ContainerTapEvent):
        global current_pokemon
        if e.control == superior_arrow:
            current_pokemon +=1
        else:
            current_pokemon -=1

        num = (current_pokemon%1000)+1
        result = await request(f"https://pokeapi.co/api/v2/pokemon/{num}")

        data = f"Name: {result['name']}\n\nAbilities: "
        for abilitieElement in result['abilities']:
            abilitie = abilitieElement['ability']['name']
            data += f"\n{abilitie}"
        data += f"\n\nHeigth: {result['height']}"
        
        text.value = data
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{num}.png"
        image.src = sprite_url
        await page.update_async()

    blue_btn = ft.Stack(
        [
            ft.Container(width=80, height=80, bgcolor=ft.colors.WHITE, border_radius=40),
            ft.Container(width=70, height=70, left=5, top=4, bgcolor=ft.colors.BLUE, border_radius=40)
        ]
    )

    items_superior =[
        ft.Container(blue_btn, width=80, height=80),
        ft.Container(width=40, height=40, bgcolor=ft.colors.YELLOW_900, border_radius=50),
        ft.Container(width=25, height=25, bgcolor=ft.colors.GREEN, border_radius=50),
        ft.Container(width=25, height=25, bgcolor=ft.colors.RED_200, border_radius=50),
    ]

    sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/0.png"
    image = ft.Image(
            src=sprite_url,
            scale=7,
            width=40,
            height=48,
            top=350/2,
            right=550/2,
        )
    stack_central = ft.Stack(
        [
            ft.Container(width=580, height=400, bgcolor=ft.colors.WHITE24, border_radius=25),
            ft.Container(width=520, height=350, bgcolor=ft.colors.GREY_900, top=25, left=25),
            image,
        ]
    )

    triangule = ft.canvas.Canvas(
        [
            ft.canvas.Path([
                ft.canvas.Path.MoveTo(40, 0),
                ft.canvas.Path.LineTo(0, 50),
                ft.canvas.Path.LineTo(80, 50)
            ],
            paint = ft.Paint(
                style = ft.PaintingStyle.FILL,
            ),
        )
    ],
        width=80,
        height=50,
    )

    superior_arrow = ft.Container(triangule, width=80, height=50, on_click=event)

    arrows = ft.Column(
        [
            superior_arrow,

            ft.Container(triangule, rotate=ft.Rotate(angle=3.14159), width=80, height=50, on_click=event)
        ]
    )

    text = ft.Text(
        value="...",
        color = ft.colors.BLACK,
        size=22,
        animate_offset=25
    )

    items_inferior = [
        ft.Container(width=50, ),
        ft.Container(text, padding=10, width=400, height=300, bgcolor=ft.colors.GREEN_400, border_radius=20),
        ft.Container(width=30, ),
        ft.Container(arrows, width=80, height=120),

    ]

    superior = ft.Container(content=ft.Row(items_superior), width=600,height=80, margin=ft.margin.only(top=40))
    center = ft.Container(content=stack_central, width=600,height=400, margin=ft.margin.only(top=40), alignment=ft.alignment.center)
    inferior = ft.Container(content=ft.Row(items_inferior), width=600,height=400, margin=ft.margin.only(top=40))

    col = ft.Column(spacing=0, controls=[
        superior,
        center,
        inferior
    ])

    container = ft.Container(col, padding=5,width=720, height=1280, bgcolor=('#C03F58'), alignment=ft.alignment.top_center)

    await page.add_async(container)
    
ft.app(target=main)

