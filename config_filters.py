#!/usr/bin/python3
# -*- coding:utf-8 -*-

from libs.filters import Filters

"""
Type        Explication                                         Filtre

fonction    Prix minimum des contrats                           Filters.PriceMin(int)
fonction    Prix maximum des contrats                           Filters.PriceMax(int)
fonction    Échéance maximum du contrat en mois                 Filters.RemainingTimeMin(int)
fonction    Échéance minimum du contrat en mois                 Filters.RemainingTimeMax(int)
fonction    Rentabilité minimum du contract en pourcentage      Filters.ROIMin(int)
fonction    Rentabilité maximum du contract en pourcentage      Filters.ROIMax(int)
classe      Pays                                                Filters.Countries.{Estonia|Finland|Germany|Latvia|Lithuania|Portugal|Spain|Sweden}
classe      État du contrat                                     Filters.ContractStates.{Funded|Late|Default}
classe      Type de paiement du contrat                         Filters.PaymentTypes.{Bullet|FullBullet|Annuity}
classe      Type de projet                                      Filters.ProjectTypes.{Bridge|Development|Business|SaleAdvanced|Refinancing|Construction|Reconstruction}

Pour les fonctions, remplacer "int" par un nombre entier.

Pour les classes, remplacer {X|Y} par X ou Y au choix. par exemple :
    Filters.ContractStates.{Funded|Late|Default}
    peut devenir :
    Filters.ContractStates.Default
"""

filters = [
    Filters.ContractStates.Funded,
    Filters.RemainingTimeMax(18),
    Filters.PriceMax(60),
    Filters.ROIMin(15),
]
