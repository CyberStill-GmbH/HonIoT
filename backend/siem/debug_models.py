# debug_models.py
import sys
import pkgutil
import inspect

print("PYTHONPATH:", sys.path[:3])

# mostrar módulos importados relacionados
mods = [m for m in sys.modules.keys() if "model" in m or "siem" in m or "backend" in m]
print("Módulos cargados que contienen 'model'/'siem'/'backend':")
for m in sorted(mods):
    print("  ", m)

# intenta importar y mostrar ubicación de ApiToken si existe
try:
    from backend.siem import models as m1
    print("\nbackend.siem.models ->", getattr(m1, "__file__", "??"))
    if hasattr(m1, "ApiToken"):
        print(" ApiToken definido en:", inspect.getsourcefile(m1.ApiToken))
    else:
        print(" ApiToken no está en backend.siem.models")
except Exception as e:
    print("Error import backend.siem.models:", e)

# intenta importarlo por nombre simple
try:
    import siem.models as m2
    print("\nsiem.models ->", getattr(m2, "__file__", "??"))
    if hasattr(m2, "ApiToken"):
        print(" ApiToken definido en:", inspect.getsourcefile(m2.ApiToken))
    else:
        print(" ApiToken no está en siem.models")
except Exception as e:
    print("siem.models no importable:", e)

# mostrar tablas registradas en metadata si alcanzable
try:
    from backend.siem.models import Base
    print("\nTablas registradas en Base.metadata:")
    for t in Base.metadata.tables:
        print("  ", t)
except Exception as e:
    print("No pude leer Base.metadata:", e)
