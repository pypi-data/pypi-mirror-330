from typing import Union, Optional, Dict
from datetime import date
from typing import Dict, Optional, List, Union
from sipametrics.base_client import BaseClient
from sipametrics.enums import Products, Apps
from sipametrics.internal.translators import (
    indices_catalogue_translation,
    metrics_translation,
    infra_equity_comparable_translation,
    infra_debt_comparable_translation,
    private_equity_comparable_boundaries_translation,
    term_structure_translation,
    taxonomies_translation,
    private_equity_comparable_translation,
)
from sipametrics.endpoints import (
    METRICS_URL,
    INFRA_EQUITY_COMPARABLE_URL,
    INFRA_DEBT_COMPARABLE_URL,
    TERMSTRUCTURE_URL,
    PRIVATE_EQUITY_COMPARABLE_URL,
    PRIVATE_EQUITY_COMPARABLE_BOUNDARIES_URL,
    INDICES_CATALOGUE_URL,
    COUNTRIES_URL,
    PRIVATE_EQUITY_REGION_TREE_URL,
)


class SipaMetricsService:
    def __init__(self, api_key: str, api_secret: str):
        self.client = BaseClient(api_key, api_secret)

    async def close(self):
        await self.client.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, tb):
        await self.client.close()

    async def metrics(self, entity_id: Union[List[str], str], metric_id: Union[List[str], str]):
        """Returns the requested metrics."""
        params = await metrics_translation(entity_id, metric_id)
        return await self.client._post(METRICS_URL, data=params)

    async def infra_equity_comparable(
        self,
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
    ) -> Dict:
        """
        Perform a comparable computation for private infra equity. This involves finding datapoints which have similar TICCS classifications and factor values (the comparables dataset) and averaging the metric values.
        """
        params = await infra_equity_comparable_translation(
            metric=metric,
            currency=currency,
            age_in_months=age_in_months,
            end_date=end_date,
            window_in_years=window_in_years,
            industrial_activities=industrial_activities,
            business_risk=business_risk,
            corporate_structure=corporate_structure,
            countries=countries,
            size=size,
            leverage=leverage,
            profitability=profitability,
            investment=investment,
            time_to_maturity=time_to_maturity,
        )
        return await self.client._post(INFRA_EQUITY_COMPARABLE_URL, data=params)

    async def infra_debt_comparable(
        self,
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
        time_to_maturity: Optional[str] = None,
    ) -> Dict:
        """
        Perform a comparable computation for private infra debt. This involves finding datapoints which have similar TICCS classifications and factor values (the comparables dataset) and averaging the metric values
        """
        params = await infra_debt_comparable_translation(
            metric=metric,
            currency=currency,
            age_in_months=age_in_months,
            end_date=end_date,
            window_in_years=window_in_years,
            industrial_activities=industrial_activities,
            business_risk=business_risk,
            corporate_structure=corporate_structure,
            countries=countries,
            face_value=face_value,
            debt_time_to_maturity=time_to_maturity,
        )
        return await self.client._post(INFRA_DEBT_COMPARABLE_URL, data=params)

    async def term_structure(self, country: str, date: date, maturity_date: date) -> Dict:
        """Query annualised risk-free rate for a given country and maturity date on the curve."""
        params = await term_structure_translation(
            country=country,
            date=date,
            maturity_date=maturity_date,
        )
        return await self.client._post(TERMSTRUCTURE_URL, data=params)

    async def private_equity_comparable(
        self,
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
        """Perform a comparable computation for private equity. This involves finding datapoints which have similar PECCS classifications and factor values (the comparables dataset) and averaging the metric values."""
        params = await private_equity_comparable_translation(
            metric=metric,
            currency=currency,
            age_in_months=age_in_months,
            end_date=end_date,
            window_in_years=window_in_years,
            industrial_activities=industrial_activities,
            revenue_models=revenue_models,
            customer_models=customer_models,
            lifecycle_phases=lifecycle_phases,
            value_chain_types=value_chain_types,
            countries=countries,
            size=size,
            growth=growth,
            leverage=leverage,
            profits=profits,
            country_risk=country_risk,
            universe=universe,
            factor_weight=factor_weight,
            type=type,
            intersect_peccs=intersect_peccs,
        )
        return await self.client._post(PRIVATE_EQUITY_COMPARABLE_URL, data=params)

    async def private_equity_comparable_boundaries(
        self,
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
        # factor_name: Optional[str] = None,
    ) -> Dict:
        """
        Handles the request to compute private equity comparable boundaries.
        """
        params = await private_equity_comparable_boundaries_translation(
            metric=metric,
            factor_name=factor_name,
            age_in_months=age_in_months,
            end_date=end_date,
            window_in_years=window_in_years,
            industrial_activities=industrial_activities,
            revenue_models=revenue_models,
            customer_models=customer_models,
            lifecycle_phases=lifecycle_phases,
            value_chain_types=value_chain_types,
            countries=countries,
            universe=universe,
            factor_weight=factor_weight,
        )
        return await self.client._post(PRIVATE_EQUITY_COMPARABLE_BOUNDARIES_URL, data=params)

    async def indices_catalogue(self, product: Union[Products, str], app: Optional[Union[Apps, str]] = None) -> Dict:
        """Return all available indices catalogue."""
        query_params = {}

        if isinstance(product, Products):
            product_value = product.value
        elif isinstance(product, str) and product in {item.value for item in Products}:
            product_value = product
        else:
            raise ValueError(f"Invalid product: {product}")

        if isinstance(app, Apps):
            app_value = app.value
        elif isinstance(app, str) and app in {item.value for item in Apps}:
            app_value = app
        else:
            app_value = None

        query_params["product"] = product_value
        if app_value:
            additional_query = await indices_catalogue_translation(product=product_value, app=app_value)
            query_params.update(additional_query)

        return await self.client._get(INDICES_CATALOGUE_URL, params=query_params)

    async def taxonomies(self, taxonomy: str, pillar: Optional[str] = None) -> Dict:
        """Return requested taxonomies mapping."""
        url, query_params = await taxonomies_translation(taxonomy=taxonomy, pillar=pillar)

        return await self.client._get(url, params=query_params)

    async def countries(self) -> Dict:
        """Return list of countries."""
        return await self.client._get(COUNTRIES_URL)

    async def private_equity_region_tree(self) -> Dict:
        """Return hierarchical view of regions and countries."""
        return await self.client._get(PRIVATE_EQUITY_REGION_TREE_URL)
