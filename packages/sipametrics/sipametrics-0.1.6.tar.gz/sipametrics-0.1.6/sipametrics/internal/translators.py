from typing import Dict, Optional, List, Union
from datetime import date
from dateutil.relativedelta import relativedelta
from sipametrics.internal.constants import COUNTRY_ISO_TO_ID_MAP, TIME_TO_MATURITY_BUCKETS, CURRENCY_MAP, TiccsProfiles
from sipametrics.enums import Products, Apps
from sipametrics.endpoints import TAXONOMIES_URL


async def metrics_translation(entity_id: Union[List[str], str], metric_id: Union[List[str], str]):
    if isinstance(entity_id, str):
        entity_id = [entity_id]
    if isinstance(metric_id, str):
        metric_id = [metric_id]
    params = {"metrics": [{"indexIds": entity_id, "typeIds": metric_id}]}
    return params


async def infra_equity_comparable_translation(
    metric: str,
    currency: Optional[str] = None,
    age_in_months: Optional[int] = None,
    end_date: Optional[date] = None,
    window_in_years: Optional[int] = None,
    industrial_activities: Optional[List[str]] = None,
    business_risk: Optional[str] = None,
    corporate_structure: Optional[str] = None,
    countries: Optional[List[str]] = None,
    size: Optional[str] = None,
    leverage: Optional[str] = None,
    profitability: Optional[str] = None,
    investment: Optional[str] = None,
    time_to_maturity: Optional[str] = None,
):
    start_date_str = _calc_start_date(end_date=end_date, window_in_years=window_in_years)
    end_date_str = end_date.strftime("%Y-%m-%d") if end_date else None

    params = {
        "metric": metric,
        "startDate": start_date_str,
        "endDate": end_date_str,
        "age": age_in_months,
    }

    ticcs_profile_map = _create_ticcs_profile_map(
        industrial_activities=industrial_activities,
        business_risk=business_risk,
        corporate_structure=corporate_structure,
    )
    params["ticcsProfiles"] = ticcs_profile_map

    factors_profile_map = _create_infra_factors_profile_map(
        currency=currency,
        countries=countries,
        size=size,
        leverage=leverage,
        profitability=profitability,
        investment=investment,
        time_to_maturity=time_to_maturity,
    )
    params["factorsProfiles"] = factors_profile_map
    return params


async def infra_debt_comparable_translation(
    metric: str,
    currency: Optional[str] = None,
    age_in_months: Optional[int] = None,
    end_date: Optional[date] = None,
    window_in_years: Optional[int] = None,
    industrial_activities: Optional[List[str]] = None,
    business_risk: Optional[str] = None,
    corporate_structure: Optional[str] = None,
    countries: Optional[List[str]] = None,
    face_value: Optional[str] = None,
    debt_time_to_maturity: Optional[str] = None,
) -> Dict:
    start_date_str = _calc_start_date(end_date=end_date, window_in_years=window_in_years)
    end_date_str = end_date.strftime("%Y-%m-%d") if end_date else None

    ticcs_profiles = _create_ticcs_profile_map(
        industrial_activities=industrial_activities,
        business_risk=business_risk,
        corporate_structure=corporate_structure,
    )

    factors_profiles = _create_infra_factors_profile_map(
        currency=currency,
        countries=countries,
        face_value=face_value,
        debt_time_to_maturity=debt_time_to_maturity,
    )

    return {
        "metric": metric,
        "startDate": start_date_str,
        "endDate": end_date_str,
        "age": age_in_months,
        "ticcsProfiles": ticcs_profiles,
        "factorsProfiles": factors_profiles,
    }


async def term_structure_translation(country: str, date: date, maturity_date: date):
    value_date_str = date.strftime("%Y-%m-%d")
    maturity_date_str = maturity_date.strftime("%Y-%m-%d")
    params = {"countryName": country, "valueDate": value_date_str, "maturityDate": maturity_date_str}
    return params


async def private_equity_comparable_translation(
    metric: str,
    currency: Optional[str] = None,
    age_in_months: Optional[int] = None,
    end_date: Optional[date] = None,
    window_in_years: Optional[int] = None,
    industrial_activities: Optional[List[str]] = None,
    revenue_models: Optional[List[str]] = None,
    customer_models: Optional[List[str]] = None,
    lifecycle_phases: Optional[List[str]] = None,
    value_chain_types: Optional[List[str]] = None,
    countries: Optional[List[str]] = None,
    size: Optional[str] = None,
    growth: Optional[str] = None,
    leverage: Optional[str] = None,
    profits: Optional[str] = None,
    country_risk: Optional[List[str]] = None,
    universe: Optional[str] = None,
    factor_weight: Optional[str] = None,
    type: Optional[str] = "mean",
    intersect_peccs: Optional[bool] = None,
) -> Dict:
    start_date_str = _calc_start_date(end_date=end_date, window_in_years=window_in_years)
    end_date_str = end_date.strftime("%Y-%m-%d") if end_date else None

    peccs_country_profile = {
        "industrialActivities": industrial_activities,
        "revenueModel": revenue_models,
        "customerModel": customer_models,
        "lifecyclePhases": lifecycle_phases,
        "valueChainTypes": value_chain_types,
        "countries": countries,
    }
    peccs_country_profile = {key: value for key, value in peccs_country_profile.items() if value is not None}

    factors_profiles = _create_equity_factors_profile_map(
        size=size,
        growth=growth,
        leverage=leverage,
        profits=profits,
        country_risk=country_risk,
    )

    params = {
        "metric": metric,
        "currency": CURRENCY_MAP.get(currency or "USD", 840),
        "startDate": start_date_str,
        "endDate": end_date_str,
        "age": age_in_months,
        "peccsCountryProfile": peccs_country_profile,
        "factorsProfiles": factors_profiles,
        "universe": universe,
        "factorWeight": factor_weight,
        "operation": type,
        "intersectPeccs": intersect_peccs,
    }

    params = {key: value for key, value in params.items() if value is not None}
    return params


async def private_equity_comparable_boundaries_translation(
    metric: str,
    factor_name: str,
    age_in_months: Optional[int] = None,
    end_date: Optional[date] = None,
    window_in_years: Optional[int] = None,
    industrial_activities: Optional[List[str]] = None,
    revenue_models: Optional[List[str]] = None,
    customer_models: Optional[List[str]] = None,
    lifecycle_phases: Optional[List[str]] = None,
    value_chain_types: Optional[List[str]] = None,
    countries: Optional[List[str]] = None,
    universe: Optional[str] = None,
    factor_weight: Optional[float] = None,
) -> Dict:

    start_date_str = _calc_start_date(end_date=end_date, window_in_years=window_in_years)
    end_date_str = end_date.strftime("%Y-%m-%d") if end_date else None

    peccs_country_profile = {
        "industrialActivities": industrial_activities,
        "revenueModel": revenue_models,
        "customerModel": customer_models,
        "lifecyclePhases": lifecycle_phases,
        "valueChainTypes": value_chain_types,
        "countries": countries,
    }
    peccs_country_profile = {key: value for key, value in peccs_country_profile.items() if value is not None}

    params = {
        "metric": metric,
        "ageInMonths": age_in_months,
        "startDate": start_date_str,
        "endDate": end_date_str,
        "universe": universe,
        "factorWeight": factor_weight,
        "factorName": factor_name,
        "peccsCountryProfile": peccs_country_profile,
    }
    params = {key: value for key, value in params.items() if value is not None}

    return params


async def taxonomies_translation(taxonomy: str, pillar: Optional[str] = None):
    url = TAXONOMIES_URL.format(taxonomy=taxonomy)
    query_params = {"pillar": pillar} if pillar is not None else {}
    return url, query_params


async def indices_catalogue_translation(product: str, app: str) -> Dict:
    app_filter_map = {
        Apps.INDICES.value: {"marketIndices": 1} if product == Products.PRIVATE_EQUITY.value else {"indexApp": 1},
        Apps.VALUATION.value: {"analytics": 1} if product == Products.PRIVATE_EQUITY.value else {"assetValuation": 1},
        Apps.CLIMATE.value: {"indexApp": 1, "assetValuation": 1},
    }
    return app_filter_map.get(app, {})


def _create_ticcs_profile_map(
    industrial_activities: Optional[List[str]] = None,
    business_risk: Optional[str] = None,
    corporate_structure: Optional[str] = None,
) -> List:
    ticcs_profile_map = {}
    if industrial_activities:
        ticcs_profile_map[TiccsProfiles.INDUSTRIAL_SUPERCLASS.value] = industrial_activities
    if business_risk:
        ticcs_profile_map[TiccsProfiles.BUSINESS_MODEL.value] = business_risk
    if corporate_structure:
        ticcs_profile_map[TiccsProfiles.CORPORATE_STRUCTURE.value] = corporate_structure

    return [{"profile": {key: value}} for key, value in ticcs_profile_map.items()]


def _create_equity_factors_profile_map(
    size: Optional[str] = None,
    growth: Optional[str] = None,
    leverage: Optional[str] = None,
    profits: Optional[str] = None,
    country_risk: Optional[List[str]] = None,
) -> List:
    factors_profiles = []

    if size:
        if size[0] == "Q":
            factors_profiles.append(
                {
                    "factorName": "Size",
                    "quintile": _convert_to_quintile(size),
                }
            )
        else:
            factors_profiles.append(
                {
                    "factorName": "Size",
                    "Size": size,
                }
            )
    if growth:
        if growth[0] == "Q":
            factors_profiles.append(
                {
                    "factorName": "Growth",
                    "quintile": _convert_to_quintile(growth),
                }
            )
        else:
            factors_profiles.append(
                {
                    "factorName": "Growth",
                    "growth": growth,
                }
            )
    if leverage:
        if leverage[0] == "Q":
            factors_profiles.append(
                {
                    "factorName": "Leverage",
                    "quintile": _convert_to_quintile(leverage),
                }
            )
        else:
            factors_profiles.append(
                {
                    "factorName": "Leverage",
                    "leverage": leverage,
                }
            )
    if profits:
        if profits[0] == "Q":
            factors_profiles.append(
                {
                    "factorName": "Profits",
                    "quintile": _convert_to_quintile(profits),
                }
            )
        else:
            factors_profiles.append(
                {
                    "factorName": "Profits",
                    "profits": profits,
                }
            )
    if country_risk:
        factors_profiles.append(
            {
                "factorName": "TermSpread",
                "countries": country_risk,
            }
        )

    return factors_profiles


def _create_infra_factors_profile_map(
    currency: Optional[str] = None,
    countries: Optional[List[str]] = None,
    size: Optional[str] = None,
    leverage: Optional[str] = None,
    profitability: Optional[str] = None,
    investment: Optional[str] = None,
    time_to_maturity: Optional[str] = None,
    debt_time_to_maturity: Optional[str] = None,
    face_value: Optional[str] = None,
) -> List:
    factors_profiles = []
    if countries:
        converted_countries = [COUNTRY_ISO_TO_ID_MAP.get(country, "Unknown") for country in countries]
        factors_profiles.append(
            {
                "profile": {
                    "factor": "countries",
                    "countries": converted_countries,
                }
            }
        )
    if size:
        if size[0] == "Q":
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "size",
                        "quintile": _convert_to_quintile(size),
                        "currency": CURRENCY_MAP.get(currency or "USD", 840),
                    }
                }
            )
        else:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "size",
                        "size": size,
                        "currency": CURRENCY_MAP.get(currency or "USD", 840),
                    }
                }
            )

    if leverage:
        if leverage[0] == "Q":
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "leverage",
                        "quintile": _convert_to_quintile(leverage),
                    }
                }
            )
        else:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "leverage",
                        "leverage": leverage,
                    }
                }
            )

    if profitability:
        if profitability[0] == "Q":
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "profitability",
                        "quintile": _convert_to_quintile(profitability),
                    }
                }
            )
        else:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "profitability",
                        "profitability": profitability,
                    }
                }
            )

    if investment:
        if investment[0] == "Q":
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "investment",
                        "quintile": _convert_to_quintile(investment),
                    }
                }
            )
        else:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "investment",
                        "investment": investment,
                    }
                }
            )

    if time_to_maturity:
        if time_to_maturity[0] == "T":
            _validate_time_to_maturity_buckets(time_to_maturity)
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "timeToMaturity",
                        "timeToMaturityBucket": _convert_to_time_series(time_to_maturity),
                    }
                }
            )
        else:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "timeToMaturity",
                        "timeToMaturity": time_to_maturity,
                    }
                }
            )

    if debt_time_to_maturity:
        if debt_time_to_maturity[0] == "T":
            _validate_time_to_maturity_buckets(debt_time_to_maturity)
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "debtTimeToMaturity",
                        "timeToMaturityBucket": _convert_to_time_series(debt_time_to_maturity),
                    }
                }
            )
        else:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "debtTimeToMaturity",
                        "timeToMaturity": debt_time_to_maturity,
                    }
                }
            )

    if face_value:
        if face_value[0] == "Q":
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "faceValue",
                        "quintile": _convert_to_quintile(face_value),
                    }
                }
            )
        else:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "faceValue",
                        "faceValue": face_value,
                    }
                }
            )

    return factors_profiles


def _convert_to_quintile(value: str):
    if value.upper().startswith("Q"):
        return int(value[1:])
    else:
        return float(value) if value.isdigit() else value


def _convert_to_time_series(value: str):
    if value.upper().startswith("T"):
        return TIME_TO_MATURITY_BUCKETS.get(value, value)
    else:
        return float(value) if value.isdigit() else value


def _validate_time_to_maturity_buckets(value: str):
    if value not in TIME_TO_MATURITY_BUCKETS:
        raise ValueError(
            f"Invalid time-to-maturity value: {value}. Valid bucket options are: {list(TIME_TO_MATURITY_BUCKETS.keys())}"
        )


def _calc_start_date(end_date: Optional[date], window_in_years: Optional[int]) -> Optional[str]:
    if end_date and window_in_years:
        start_date = end_date - relativedelta(years=window_in_years)
        return start_date.strftime("%Y-%m-%d")
    return None
