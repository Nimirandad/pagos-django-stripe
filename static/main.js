fetch("/config/").then((result) => {
    return result.json();
}).then((data) => {
    const stripe = Stripe(data.publicKey);
    console.log(stripe);

    document.querySelector("#submitBtn").addEventListener("click", () => {

        fetch("/pago-orden/")
            .then((result) => { return result.json(); })
            .then((data) => {
                console.log(data);

                return stripe.redirectToCheckout({ sessionId: data.sessionId })
            })
            .then((res) => {
                console.log(res);
            });
    });
});