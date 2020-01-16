from django.utils.translation import gettext as _

NIVELES_PELIGRO = (
    ("Bajo", _("Bajo")),
    ("Medio", _("Medio")),
    ("Alto", _("Alto"))
)

PROCESOS = (
    (None, _("---")),
    ("DA", _("DA")),
    ("MEC", _("MEC")),
    ("FBR", _("FBR"))
)
