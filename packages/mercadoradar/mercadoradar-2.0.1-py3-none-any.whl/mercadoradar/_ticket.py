from typing import Optional

from ._api import MercadoRadarAPI
from ._models.ticket import Ticket as TicketSchema
from .enums import TicketCategory


class Ticket:

    @classmethod
    def create(cls,
               title: str,
               description: str,
               customer_id: Optional[int] = None,
               customer_email: Optional[str] = None,
               category: Optional[TicketCategory] = None,
               links: Optional[list[str]] = None) -> TicketSchema:
        """
        Creates a new ticket in the MercadoRadar

        :param title: The title of the ticket
        :param description: Detailed description of the issue
        :param customer_id: The id of the customer creating the ticket
        :param customer_email: The email of the customer creating the ticket
        :param category: The category of the ticket (optional)
        :param links: A list of related links (optional)

        :return: Ticket instance with the created ticket data
        """

        api = MercadoRadarAPI()
        data = dict(
            title=title,
            description=description,
            customer_email=customer_email,
            customer_id=customer_id,
            category=category.value if category else None,
            links=links or []
        )

        ticket_response = api.create_request(path='/v3/ticket/', data=data)

        return TicketSchema(**ticket_response)
