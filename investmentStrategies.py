import pandas as pd

MONTH_YEAR = 12

def lump_sum_approach(df, purchase_dates, horizon: int):
    """
    Retourne le ROI d'un investissement de type LumpSum pour une série de dates d'achat.

    :param df: DataFrame pandas avec des dates de trading en index et des valeurs d'actions au closing en colonnes.
    :param purchase_dates: Série de dates d'achat (format string 'YYYY-MM-DD' ou datetime).
    :param horizon: Horizon d'investissement en mois (int).
    :return: Série de ROI de l'investissement.
    """
    # Convertir les dates d'achat en format datetime si nécessaire
    purchase_dates = pd.to_datetime(purchase_dates)

    # Calculer les dates cibles basées sur l'horizon d'investissement
    target_dates = purchase_dates + pd.DateOffset(months=horizon)

    # Trouver les dates de trading les plus proches pour chaque target_date
    target_dates = df.index.searchsorted(target_dates)
    target_dates = df.index[target_dates]

    # Calculer le ROI pour chaque date
    annualization_power = MONTH_YEAR / horizon
    roi = (df.loc[target_dates].values / df.loc[purchase_dates].values) ** annualization_power - 1

    return pd.Series(roi, index=purchase_dates)


def dollar_average_cost_approach(df, purchase_dates, horizon: int, frequency: int):
    """
    Retourne le ROI d'un investissement de type Dollar Average Cost pour une série de dates d'achat.

    :param df: DataFrame pandas avec des dates de trading en index et des valeurs d'actions au closing en colonnes.
    :param purchase_dates: Série de dates d'achat (format string 'YYYY-MM-DD' ou datetime).
    :param horizon: Horizon d'investissement en mois (int).
    :param frequency: Fréquence d'investissement en mois (int).
    :return: Série de ROI de l'investissement.
    """
    # Convertir les dates d'achat en format datetime si nécessaire
    purchase_dates = pd.to_datetime(purchase_dates)

    # Calculer les dernières dates basées sur l'horizon d'investissement
    last_dates = purchase_dates + pd.DateOffset(months=horizon)

    # Trouver les dates de trading les plus proches pour chaque last_date
    last_dates = df.index.searchsorted(last_dates)
    last_dates = df.index[last_dates]
    last_closing_values = df.loc[last_dates].values

    # Calculer le nombre de transactions basées sur l'horizon et la fréquence
    nb_transactions = horizon // frequency

    # Générer un DataFrame pour toutes les dates d'investissement intermédiaires
    colnames_transac = range(nb_transactions)
    df_idx = pd.DataFrame(0, index = purchase_dates, columns = colnames_transac)
    for colname in colnames_transac:
        purchase_dates_temp = purchase_dates + pd.DateOffset(months = colname * frequency)
        purchase_dates_temp = df.index[df.index.searchsorted(purchase_dates_temp)]
        purchase_idx_temp   = 1 / df.loc[purchase_dates_temp]
        df_idx[colname] = purchase_idx_temp.to_list()

    # Calculer le ROI moyen pour chaque achat initial
    annualization_power = MONTH_YEAR / horizon

    df_mean = df_idx.mean(axis = 1)
    df_mean = (df_mean * last_closing_values) ** annualization_power - 1

    return df_mean
