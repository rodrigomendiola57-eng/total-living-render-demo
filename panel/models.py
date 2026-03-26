from django.db import models


class NosotrosContent(models.Model):
    hero_title = models.CharField(max_length=120, default='Filosofía Total')
    hero_line_1 = models.CharField(
        max_length=220,
        default='En el sector inmobiliario sobran promesas y faltan procesos.',
    )
    hero_line_2 = models.CharField(max_length=220, default='Nosotros elegimos método TOTAL.')

    pillar_1 = models.CharField(max_length=140, default='No improvisamos')
    pillar_2 = models.CharField(max_length=140, default='No vendemos por presión')
    pillar_3 = models.CharField(max_length=140, default='Tomamos decisiones con datos')
    pillar_4 = models.CharField(max_length=140, default='Ejecutamos con orden')
    pillar_5 = models.CharField(max_length=140, default='Respuesta ágil y seguimiento real')
    pillar_6 = models.CharField(max_length=140, default='Documentación clara en cada etapa')
    pillar_7 = models.CharField(max_length=140, default='Trabajo coordinado entre especialistas')
    pillar_8 = models.CharField(max_length=140, default='Negociación enfocada en rentabilidad')

    manifest_title = models.CharField(max_length=140, default='Manifiesto T.O.T.A.L')
    manifest_t_meaning = models.CharField(max_length=140, default='Transparencia')
    manifest_t_desc = models.CharField(max_length=220, default='Comunicación clara y honesta.')
    manifest_o_meaning = models.CharField(max_length=140, default='Orden')
    manifest_o_desc = models.CharField(max_length=220, default='Procesos definidos en cada etapa.')
    manifest_t2_meaning = models.CharField(max_length=140, default='Trazabilidad')
    manifest_t2_desc = models.CharField(max_length=220, default='Seguimiento visible y documentado.')
    manifest_a_meaning = models.CharField(max_length=140, default='Acompañamiento real')
    manifest_a_desc = models.CharField(
        max_length=320,
        default='Del primer mensaje a la firma y después: seguimiento cercano en cada paso del proceso.',
    )
    manifest_l_meaning = models.CharField(max_length=140, default='Lealtad al cliente')
    manifest_l_desc = models.CharField(
        max_length=320,
        default='Tu interés primero, con negociación firme y criterio profesional en cada decisión.',
    )

    mission_vision_title = models.CharField(max_length=140, default='Misión y visión')
    mission_title = models.CharField(max_length=80, default='Misión')
    mission_text = models.TextField(
        default='Convertir cada operación inmobiliaria en una decisión clara, segura y rentable, '
                'mediante asesoría profesional y multidisciplinaria, con transparencia, orden y '
                'estrategia en cada etapa del proceso.'
    )
    vision_title = models.CharField(max_length=80, default='Visión')
    vision_text = models.TextField(
        default='Ser la alternativa que pone orden y certeza donde otros improvisan, integrando '
                'decisiones con datos, seguimiento real y negociación estratégica en todo el mercado inmobiliario.'
    )

    team_banner_title = models.CharField(max_length=140, default='Equipo Total Living')

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Configuración Nosotros'
