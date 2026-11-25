"""Página "Historia" de travellingskates.com.

Fuentes del contenido: la historia publicada en nicolasveigapalacios.com, el material del
repositorio Travelling-Skates-Factory-Skates (renders, planos, fotos de producción y prensa)
y el catálogo del sitio original.
"""
import html

TITLE = 'Nuestra historia'
DESC = ('La historia de Travelling Skates S.A.: cómo nacieron las ruedas Quantum y nuestras planchas, '
        'el proceso de ingeniería, matricería e inyección, y los reconocimientos recibidos.')
IMG = 'assets/historia/'


def esc(s):
    return html.escape(s, quote=True)


def fig(name, cap, group, cls=''):
    src = IMG + name + '.jpg'
    return (f'<figure class="h-fig {cls}" data-lb="{group}" data-src="{src}" data-title="{esc(cap)}" data-desc="">'
            f'<img src="{src}" alt="{esc(cap)}" loading="lazy"><figcaption>{esc(cap)}</figcaption></figure>')


def video(vid, title):
    return (f'<div class="h-video"><button class="yt-lite" data-yt="{vid}" aria-label="Reproducir: {esc(title)}" '
            f'style="background-image:url(https://i.ytimg.com/vi/{vid}/hqdefault.jpg)"><span class="yt-play"></span></button>'
            f'<p>{esc(title)}</p></div>')


TIMELINE = [
    ('fucsia', 'El comienzo',
     'Nicolás E. Veiga Palacios funda Travelling Skates S.A. para fabricar en Argentina equipamiento de alto rendimiento '
     'para patinaje artístico, y crea Argentina Technology Group SRL para desarrollar la tecnología de las planchas.'),
    ('violeta', 'La primera prueba',
     'Cerca del 20% de las primeras planchas fabricadas presentó problemas estructurales. Todas fueron reemplazadas, '
     'pero en un deporte de alto rendimiento una sola falla en la pista puede costar años de confianza. Al mismo tiempo, '
     'la ingeniería y el diseño de los moldes eran sólidos, pero faltaba experiencia en producción en serie, y una red que '
     'aportaba capital de trabajo dejó de pagar.'),
    ('celeste', 'El giro: las ruedas',
     'La decisión fue cambiar el flujo de caja: acelerar el desarrollo de ruedas, un producto de ciclo más corto y demanda '
     'más previsible. La producción se hizo junto a Kollplast SRL, con más de 20 años abasteciendo a la industria '
     'automotriz, priorizando calidad y confiabilidad por sobre el ahorro de corto plazo.'),
    ('fucsia', 'Nacen las Quantum',
     'En solo cinco meses (ingeniería, matricería y puesta en marcha de la producción) se lanzaron las ruedas Quantum, '
     'fabricadas con elastómero DuPont importado de Estados Unidos. Sin presupuesto de marketing, se presentaron '
     'directamente a patinadores y entrenadores en una competencia nacional. La respuesta fue inmediata y la demanda '
     'superó lo previsto.'),
    ('violeta', 'De pie otra vez',
     'Las ruedas estabilizaron la caja, permitieron pagar el 100% de la deuda y recuperar la confianza de la comunidad del '
     'patinaje. Con esa base se corrigieron los errores, se ajustaron los procesos y se relanzó la línea de planchas sin '
     'fallas técnicas.'),
    ('celeste', 'Crecimiento',
     'Llegó una etapa de crecimiento controlado: más productos, operaciones profesionalizadas, programas de apoyo '
     'públicos y privados, y distribución en Argentina y Sudamérica, compitiendo de igual a igual con marcas europeas '
     'de larga trayectoria.'),
]

PRODUCTS = [
    ('Ruedas', 'gallery.html', 'Quantum 57, Quantum Gold y Silver, Figuras 63, PINK! y la línea Quantum Pro, Dance y Derby.',
     'producto-ruedas-packs'),
    ('Planchas', 'planchas.html', 'Planchas de diseño propio, desarrolladas en CAD y probadas talle por talle.',
     'producto-plancha-dorada'),
    ('Frenos', 'frenos.html', 'Frenos rosca europea en fucsia, violeta, celeste y blanco.', 'producto-plancha-rueda'),
    ('Suspensiones', 'suspenciones.html', 'Suspensiones de goma y de poliuretano en los colores de la marca.',
     'producto-plancha-suspensiones'),
    ('Rodamientos', 'rodamientos.html', 'Rodamientos para completar cada patín.', 'producto-rueda-mano'),
    ('Patines completos', 'patines-completos.html', 'Bota, plancha, ruedas y freno: el patín armado y listo.',
     'producto-patin-completo'),
]

AWARDS = [
    ('2013', 'Ganador del Programa Capital Semilla',
     'Secretaría de la Pequeña y Mediana Empresa (SEPyME), Ministerio de Industria.',
     'https://cdi.mecon.gob.ar/bases/docelec/fc1480.pdf'),
    ('2015', 'FONTAR ANR 2200',
     'Aporte no reembolsable de la Agencia Nacional de Promoción Científica y Tecnológica (Ministerio de Ciencia).',
     'http://www.agencia.mincyt.gob.ar/upload/Res010-16-ANR%202200%202015%20C2-Evaluaci%C3%B3n-Aprobados%20con%20modificacion.pdf'),
    ('2015', 'Puesto 10 · Joven Empresario Industrial',
     'Ranking de la revista Bien Argentino, del Ministerio de Industria de la Nación.',
     'https://issuu.com/diegocolombres/docs/revista_bien_argentino_ministerio_d'),
]


def body():
    t = []
    a = t.append
    # hero
    a('<section class="h-hero">'
      '<div class="h-hero-img" style="background-image:url(' + "'" + IMG + 'planchas-doradas-produccion.jpg' + "'" + ')"></div>'
      '<div class="h-wrap h-hero-txt"><p class="h-kicker">TRAVELLING SKATES S.A.</p>'
      '<h1>Nuestra historia</h1>'
      '<p class="h-lead">La marca de patín artístico líder en Latinoamérica, con más de 13 años en el mercado. '
      'Investigación de materiales y tecnología de fabricación propias para atletas que compiten al más alto nivel.</p>'
      '<div class="h-dots"><span class="d-fucsia"></span><span class="d-violeta"></span><span class="d-celeste"></span><span class="d-gris"></span></div>'
      '</div></section>')
    # intro with founder
    a('<section class="h-wrap h-intro">'
      + fig('nicolas-veiga-palacios-productos', 'Nicolás E. Veiga Palacios, fundador de Travelling Skates', 'hist-intro', 'h-intro-fig') +
      '<div><h2>Un atleta increíble, necesita productos increíbles.</h2>'
      '<p>Travelling Skates nació en Argentina para fabricar equipamiento de alto rendimiento para patinaje artístico, '
      'hockey sobre ruedas y roller derby: ruedas, planchas, frenos, suspensiones y rodamientos.</p>'
      '<p>No se construyó en condiciones ideales. Se construyó bajo presión, con incertidumbre técnica, restricciones '
      'financieras y riesgo de reputación. Su recorrido no se definió por evitar errores, sino por detectarlos a tiempo, '
      'hacerse cargo y reestructurar con decisión.</p></div></section>')
    # timeline
    a('<section class="h-band"><div class="h-wrap"><h2 class="h-title">El camino</h2><ol class="h-timeline">')
    for color, title, text in TIMELINE:
        a(f'<li><span class="h-dot d-{color}"></span><h3>{esc(title)}</h3><p>{esc(text)}</p></li>')
    a('</ol></div></section>')
    # process: wheels
    a('<section class="h-wrap h-sec"><p class="h-kicker">PROCESO</p><h2 class="h-title">Así nace una rueda</h2>'
      '<p class="h-text">Cada rueda empieza en la pantalla. Se dibujaron varias propuestas de diseño para la rueda de 57 mm, '
      'se estudiaron las pisadas de 31 y 35 mm para la de 63 mm y se pasó a planos de fabricación. Después vinieron el '
      'molde y la inyección con elastómero DuPont.</p>'
      '<h3 class="h-sub">1 · Diseño y renders</h3><div class="h-grid g4">')
    for i in range(1, 5):
        a(fig(f'rueda-propuesta-{i}', f'Rueda Ø57, propuesta de diseño {i}', 'hist-ruedas'))
    a('</div><div class="h-grid g2">')
    a(fig('rueda-d63-pisada-31', 'Rueda Ø63, pisada de 31 mm', 'hist-ruedas'))
    a(fig('rueda-d63-pisada-35', 'Rueda Ø63, pisada de 35 mm', 'hist-ruedas'))
    a('</div><h3 class="h-sub">2 · Planos</h3><div class="h-grid g2">')
    a(fig('plano-ruedas', 'Plano de ruedas: original de inyección y diámetros 63, 57 y 31', 'hist-ruedas'))
    a(fig('plano-ruedas-perfil', 'Plano de rueda: vistas y perfiles', 'hist-ruedas'))
    a('</div><h3 class="h-sub">3 · Inyección</h3><div class="h-grid g3">')
    a(fig('kollplast-inyectora', 'Producción de ruedas en la inyectora', 'hist-ruedas'))
    a(fig('inyectora-ruedas', 'Las primeras ruedas sobre la inyectora', 'hist-ruedas'))
    a(fig('inyectora-ruedas-2', 'Ruedas recién inyectadas en los colores de la marca', 'hist-ruedas'))
    a('</div><div class="h-grid g2">')
    a(fig('ruedas-render-1', 'Línea de ruedas Travelling Skates', 'hist-ruedas'))
    a(fig('ruedas-render-2', 'Línea de ruedas Travelling Skates', 'hist-ruedas'))
    a('</div></section>')
    # process: frames
    a('<section class="h-band"><div class="h-wrap h-sec"><p class="h-kicker">PROCESO</p><h2 class="h-title">Así nace una plancha</h2>'
      '<p class="h-text">La plancha es la base del patín. Se diseñó en CAD, se modeló la base en SolidWorks, se armó '
      'virtualmente con sus suspensiones y ejes, y se escaló talle por talle, del 105 al 145. Después de corregir la '
      'primera producción, la línea se relanzó sin fallas técnicas.</p>'
      '<h3 class="h-sub">1 · Base y talles</h3><div class="h-grid g2">')
    a(fig('plano-base-patin', 'Base del patín: vistas del modelo en SolidWorks', 'hist-planchas'))
    a(fig('plancha-talles', 'Escala de talles: 105, 115, 125, 135 y 145', 'hist-planchas'))
    a('</div><div class="h-grid g3">')
    a(fig('plancha-talle-105-145', 'Talle 105 (195 mm) y talle 145 (235 mm)', 'hist-planchas'))
    a(fig('plancha-talles-frontal', 'Vista frontal de los cinco talles', 'hist-planchas'))
    a(fig('plancha-render-diseno', 'Ángulos de ejes y suspensiones', 'hist-planchas'))
    a('</div><h3 class="h-sub">2 · Conjunto armado</h3><div class="h-grid g2">')
    a(fig('plancha-conjunto-1', 'Conjunto armado: plancha, suspensiones y ejes', 'hist-planchas'))
    a(fig('plancha-conjunto-2', 'Conjunto armado, vista en perspectiva', 'hist-planchas'))
    a('</div><div class="h-grid g2">')
    a(fig('plancha-evo-2', 'Plancha Evo 2 (render)', 'hist-planchas'))
    a(fig('plancha-kinetic', 'Plancha Kinetic (render)', 'hist-planchas'))
    a('</div><h3 class="h-sub">3 · Molde y producción</h3><div class="h-grid g3">')
    a(fig('molde-plancha', 'Molde de plancha', 'hist-planchas'))
    a(fig('planchas-doradas-produccion', 'Planchas doradas armadas en producción', 'hist-planchas'))
    a(fig('producto-plancha-dorada', 'Plancha dorada con ruedas Travelling Skates', 'hist-planchas'))
    a('</div></div></section>')
    # products
    a('<section class="h-wrap h-sec"><p class="h-kicker">PRODUCTOS</p><h2 class="h-title">Todo para tu patín</h2>'
      '<div class="h-products">')
    for name, href, text, img in PRODUCTS:
        a(f'<a class="h-prod" href="{href}"><span class="h-prod-img" style="background-image:url(' + "'" + IMG + img + '.jpg' + "'" + f')"></span>'
          f'<span class="h-prod-t">{esc(name)}</span><span class="h-prod-d">{esc(text)}</span><span class="h-prod-more">Ver productos &rarr;</span></a>')
    a('</div><div class="h-grid g4 h-more">')
    a(fig('producto-ruedas-cajas', 'Ruedas Quantum en su presentación', 'hist-productos'))
    a(fig('producto-patines-pista', 'Patines con ruedas Travelling Skates en la pista', 'hist-productos'))
    a(fig('productos-1', 'Planchas, ruedas y suspensiones', 'hist-productos'))
    a(fig('productos-2', 'Planchas armadas', 'hist-productos'))
    a('</div></section>')
    # videos
    a('<section class="h-band"><div class="h-wrap h-sec"><p class="h-kicker">VIDEOS</p><h2 class="h-title">Travelling Skates en video</h2><div class="h-grid g2">')
    a(video('ze6OEQH6xF0', 'Travelling Skates en "Valor Agregado" · Programa Encuentro'))
    a(video('gU8ZA5r5Bow', 'Quantum Pro · Quantum Dance · Quantum Derby'))
    a('</div></div></section>')
    # awards & press
    a('<section class="h-wrap h-sec"><p class="h-kicker">RECONOCIMIENTOS Y PRENSA</p><h2 class="h-title">Lo que dijeron de nosotros</h2>'
      '<div class="h-awards">')
    for year, title, text, url in AWARDS:
        a(f'<a class="h-award" href="{url}" target="_blank" rel="noopener"><span class="h-award-y">{year}</span>'
          f'<span class="h-award-t">{esc(title)}</span><span class="h-award-d">{esc(text)}</span><span class="h-award-l">Ver documento &rarr;</span></a>')
    a('</div><a class="h-press" href="https://www.lanacion.com.ar/economia/sin-titulo-nid1762673/" target="_blank" rel="noopener">'
      '<span class="h-press-src">LA NACIÓN</span><span class="h-press-t">Travelling Skates en la sección Economía del diario La Nación</span>'
      '<span class="h-award-l">Leer la nota &rarr;</span></a>'
      '<div class="h-grid g4">')
    a(fig('cfk-travelling-skates', 'Cristina Fernández de Kirchner con Travelling Skates', 'hist-prensa'))
    a(fig('nicolas-uniona-georgi', 'Nicolás Veiga Palacios (izquierda), Daniel Uriona (centro) y Débora Georgi', 'hist-prensa'))
    a(fig('nicolas-emprendedores', 'Nicolás con otros emprendedores, Inés Nevárez y Carlos Lerner', 'hist-prensa'))
    a(fig('fabrica-planta', 'Planta industrial', 'hist-prensa'))
    a('</div></section>')
    # community
    a('<section class="h-band"><div class="h-wrap h-sec"><p class="h-kicker">EN LA PISTA</p><h2 class="h-title">Con los patinadores</h2>'
      '<p class="h-text">Las Quantum se presentaron directamente a patinadores y entrenadores en una competencia nacional. '
      'Desde entonces, Travelling Skates acompaña a los atletas en torneos y podios.</p><div class="h-grid g2">')
    a(fig('evento-podio', 'Podio con el stand de Travelling Skates', 'hist-pista'))
    a(fig('evento-torneo', 'Evento de patinaje', 'hist-pista'))
    a('</div></div></section>')
    # CTA
    a('<section class="h-wrap h-cta"><h2>Vive tu camino a la Gloria.</h2>'
      '<div class="h-cta-btns"><a class="h-btn h-btn-blue" href="distribuidores.html">DISTRIBUIDORES</a>'
      '<a class="h-btn h-btn-purple" href="gallery.html">VER PRODUCTOS</a></div></section>')
    return '\n'.join(t)
