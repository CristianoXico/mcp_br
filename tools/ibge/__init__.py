"""
Pacote para acesso às APIs do IBGE
"""

# Importa todas as funções de cada módulo para facilitar o acesso
from ..ibge_localidades import *
from ..ibge_agregados import *
from ..ibge_malhas import *
from ..ibge_metadados import *
from ..ibge_cnae import *
from ..ibge_nomes import *
from ..ibge_censos import *

# Novas APIs implementadas
from ..ibge_bdg import *
from ..ibge_bngb import *
from ..ibge_calendario import *
from ..ibge_hgeohnor import *
from ..ibge_noticias import *
from ..ibge_paises import *
from ..ibge_pesquisas import *
from ..ibge_ppp import *
from ..ibge_produtos import *
from ..ibge_progrid import *
from ..ibge_publicacoes import *
from ..ibge_rbmc import *
from ..ibge_rmpg import *

# Versão do pacote
__version__ = "1.0.0"
