from django.db import models
from accounts.models import User


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.full_name} -> {self.receiver.full_name}: {self.message[:50]}"


POULTRY_QA = {
    'price': 'Our prices vary by product and season. Please check the product listings for current prices.',
    'delivery': 'We deliver within 3-5 business days. Delivery time may vary by location.',
    'fresh': 'All our products are fresh and sourced directly from farms.',
    'egg': 'We have desi eggs, farm eggs, and organic eggs available in different quantities.',
    'chicken': 'We offer Desi Murgi, Sonali Chicken, Broiler Chicken, and Duck.',
    'payment': 'We accept bKash and Nagad mobile banking payments.',
    'return': 'We have a 24-hour return policy for quality issues. Please contact the seller directly.',
    'organic': 'Many of our sellers offer organically raised poultry. Look for the organic tag on products.',
    'bulk': 'Bulk orders are available. Contact the seller directly for bulk pricing.',
    'halal': 'All our poultry products are halal certified.',
    'weight': 'Products are sold by kg, piece, or mon depending on the product type.',
    'contact': 'You can contact sellers directly through their farm page.',
    'murgi': 'Desi Murgi (country chicken) is available from multiple farms. Check our listings.',
    'sonali': 'Sonali chicken is a popular hybrid breed available from our certified farms.',
}


def get_ai_response(message):
    message_lower = message.lower()
    for keyword, response in POULTRY_QA.items():
        if keyword in message_lower:
            return response
    return ("Thank you for your question! For specific inquiries, please browse our product listings "
            "or contact the seller directly through their farm page. We're here to help you find "
            "the best poultry products!")
