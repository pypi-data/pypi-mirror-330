"""Models for django-ca-cmc."""

from cryptography import x509
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ca.modelfields import CertificateField, LazyCertificate
from django_ca.utils import int_to_hex


class CMCClient(models.Model):
    """CMC client certificate."""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Key client data
    certificate = CertificateField(verbose_name=_("Client certificate"))

    # Properties of the certificate for faster data access
    not_before = models.DateTimeField(blank=False)
    not_after = models.DateTimeField(null=False, blank=False)
    serial = models.CharField(max_length=64, unique=True)

    comment = models.TextField(default="")
    copy_extensions = models.BooleanField(
        default=False,
        help_text=_(
            "Copy (almost) all extensions from the CSR if a request is signed by this certificate."
        ),
    )

    class Meta:
        verbose_name = _("CMC client")
        verbose_name_plural = _("CMC clients")

    def __str__(self) -> str:
        return self.serial

    def update_certificate(self, value: x509.Certificate) -> None:
        """
        Update instance with data from a :py:class:`cg:cryptography.x509.Certificate`.

        This function will also populate the ``serial, `not_after` and `not_before` fields.
        """
        self.certificate = LazyCertificate(value)
        self.not_after = value.not_valid_after_utc
        self.not_before = value.not_valid_before_utc

        if settings.USE_TZ is False:
            self.not_after = self.not_after.replace(tzinfo=None)
            self.not_before = self.not_before.replace(tzinfo=None)

        self.serial = int_to_hex(value.serial_number)  # upper-cased by int_to_hex()
