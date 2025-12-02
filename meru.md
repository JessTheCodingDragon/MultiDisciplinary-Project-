
sequenceDiagram
  participant C as Customer (UI)
  participant API as API Gateway
  participant Auth as AuthService
  participant Cart as CartService
  participant Order as OrderService
  participant Product as ProductService
  participant Payment as PaymentService
  participant PG as ExternalPaymentGateway
  participant Invoice as InvoiceService
  participant Notif as NotificationService
  participant DB as Database

  C->>API: Click "Checkout"
  API->>Auth: validateToken(customerToken)
  Auth-->>API: OK
  API->>Cart: getCart(customerId)
  Cart-->>API: cart(items, total)
  API->>Order: createOrderFromCart(customerId, cart)
  Order->>Product: reserveStock(items)
  Product-->>Order: reserved / fail
  alt stock reserved
    Order->>DB: persist(order, items, status=PendingPayment)
    Order-->>API: orderCreated(orderId, amount)
    API->>Payment: initiatePayment(orderId, amount, method)
    Payment->>PG: process(paymentDetails)
    PG-->>Payment: success
    Payment->>DB: persist(payment status=Paid)
    Payment-->>Order: paymentSuccess
    Order->>DB: update(status=Confirmed)
    Order->>Invoice: generate(orderId)
    Invoice-->>DB: persist(invoice)
    Invoice-->>Notif: deliverInvoice(customerEmail)
    Notif-->>C: send(order confirmation + invoice)
  else stock failed
    Order-->>API: fail(reason)
    API-->>C: show error (out of stock)
  end
