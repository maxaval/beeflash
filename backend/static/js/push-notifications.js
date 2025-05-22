if ("Notification" in window && "serviceWorker" in navigator) {
    navigator.serviceWorker.register("/static/sw.js").then(function(reg) {
        console.log("Service Worker registrado.");
    });
}

function solicitarPermiso() {
    Notification.requestPermission().then(function(permission) {
        if (permission === "granted") {
            new Notification("¡Notificación activada!", { body: "Ahora recibirás alertas en Bee Flash 🚀" });
        }
    });
}
