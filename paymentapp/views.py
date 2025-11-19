from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import razorpay
from AdminpanelApp.models import Course, Enrollment, Payment


@login_required
def create_order(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    amount = int(course.price * 100)  
    

    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    payment_order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1",  
    })

    Payment.objects.create(
        user=request.user,
        course=course,
        order_id=payment_order['id'],
        amount=amount / 100,  
        refund_amount=0.00,
        discount_applied=0.00,
        payment_status='Pending',
    )

    context = {
        'course': course,
        'amount': amount,
        'order_id': payment_order['id'],
        'razorpay_key': settings.RAZOR_KEY_ID,
    }
    return render(request, "payment_page.html", context)


@csrf_exempt
@login_required
def payment_success(request):
    if request.method == "POST":
        order_id = request.POST.get('razorpay_order_id')
        payment_id = request.POST.get('razorpay_payment_id')
        signature = request.POST.get('razorpay_signature')

        print("POST DATA:", request.POST)

        if not order_id or not payment_id or not signature:
            return redirect('paymentapp:error_page')

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)

            payment = Payment.objects.filter(order_id=order_id).first()
            if not payment:
                return redirect('paymentapp:error_page')

            payment.razorpay_signature = signature
            payment.payment_id = payment_id
            payment.payment_status = "Completed"
            payment.save()

            Enrollment.objects.get_or_create(
                user=request.user,
                course=payment.course,
                defaults={'status': 'completed'}
            )

            return redirect('home')

        except razorpay.errors.SignatureVerificationError:
            return redirect('paymentapp:error_page')

    return redirect('paymentapp:error_page')


def error_page(request):
    return HttpResponse("Error: Something went wrong.")
