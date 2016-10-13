# encoding: utf-8
__author__ = 'Nazmi ZORLU'
__email__ = "nazmizorlu@gmail.com"

from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from foursquare_client import client as fs_client


class Venue(models.Model):
    fs_id = models.CharField(verbose_name=_("Foursquare ID"), max_length=24,
                             unique=True, db_index=True)
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    phone = models.CharField(verbose_name=_("Phone Number"), max_length=20,
                             null=True, blank=True, default=None)
    checkins_count = models.IntegerField(verbose_name=_("Checkin Count"),
                                         default=0)


class Search(models.Model):
    phrase = models.CharField(verbose_name=_("Search for"), max_length=100)
    location = models.CharField(verbose_name=_("Location"), max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    venues = models.ManyToManyField(Venue, verbose_name=_("Venues"),
                                    related_name="in_searches")

    class Meta:
        ordering = ("-updated_at",)
        unique_together = ("phrase", "location")

    def collect_venues(self):
        try:
            client = fs_client.FoursquareClient(
                settings.FOURSQUARE_CLIENT_ID,
                settings.FOURSQUARE_CLIENT_SECRET)
            resp = client.venues_search(self.phrase, self.location)
            venues_list = resp["response"]["venues"]
            for item in venues_list:
                if "formattedPhone" in item["contact"]:
                    item_phone = item["contact"]["formattedPhone"]
                elif "phone" in item["contact"]:
                    item_phone = item["contact"]["phone"]
                else:
                    item_phone = None
                try:
                    venue = Venue.objects.create(
                        fs_id=item["id"],
                        name=item["name"],
                        phone=item_phone,
                        checkins_count=item["stats"]["checkinsCount"])
                except IntegrityError:
                    venue = Venue.objects.get(fs_id=item["id"])

                if self.venues.filter(fs_id=item["id"]).count() == 0:
                    self.venues.add(venue)

        except fs_client.FourSquareException:
            pass

        self.save()
