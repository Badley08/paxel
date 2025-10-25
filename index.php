<?php
// ==========================
// 🤖 Paxel - Chatbot de Karlito
// Version PHP sans dépendance externe
// ==========================

// === Identifiants Twilio ===
$account_sid = "AC229e9b5ba22977d241cb5777a1150b8d";
$auth_token  = "1db269788e312aecb882ae722647a1e7";
$twilio_whatsapp = "whatsapp:+14155238886";

// === Liste des numéros et réponses ===
$responses = [
    "+33758080294"  => "Mes salutations au père de mon créateur. Je suis Paxel, une IA créée par Karlito pour répondre à ses messages quand il n'est pas disponible. Pour l'instant, votre fils n'est pas disponible. Quand il le saura, il vous répondra.",
    "+18092820899"  => "Pour l'instant Karlito n'est pas disponible. Vu que tu es sa meilleure amie, il te répondra vite quand il verra ton message. Je suis Paxel, son AI assistant créé pour répondre à ses messages à sa place.",
    "+18097520703"  => "Je t’écrirai quand je serai disponible bby 💕.",
    "+50938576922"  => "Je suis Paxel, le chatbot de Karlito. Si je réponds à ton message à sa place, c’est qu’il n’est pas disponible pour l’instant. Quand il le sera, il te répondra.",
    "+18493957350"  => "Hola Kim, soy Paxel, el chatbot de Karlito. Si yo respondo tus mensajes en lugar de él, es porque no está disponible en este momento. En cuanto esté disponible, te responderá.",
    "default"       => "Karlito n’est pas disponible pour l’instant. Il entrera en contact avec vous dès qu’il le sera. Je suis Paxel, son chatbot créé pour répondre à sa place."
];

// === Fonction d’envoi WhatsApp Twilio ===
function sendWhatsAppMessage($to, $message, $sid, $token, $from) {
    $url = "https://api.twilio.com/2010-04-01/Accounts/$sid/Messages.json";

    $data = [
        "From" => "whatsapp:$from",
        "To" => "whatsapp:$to",
        "Body" => $message
    ];

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_USERPWD, "$sid:$token");
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));

    $result = curl_exec($ch);
    curl_close($ch);

    return $result;
}

// === Simulation de réception (webhook Twilio) ===
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $from = str_replace("whatsapp:", "", $_POST["From"] ?? "");
    $body = trim($_POST["Body"] ?? "");

    // Trouver le message à envoyer
    $reply = $responses[$from] ?? $responses["default"];

    // Délai de 30 secondes (comme demandé)
    sleep(30);

    // Envoi de la réponse
    sendWhatsAppMessage($from, $reply, $account_sid, $auth_token, $twilio_whatsapp);
    echo "✅ Réponse envoyée à $from";
    exit;
}

?>

<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Paxel - WhatsApp Chatbot</title>
</head>
<body style="font-family:Arial;text-align:center;margin-top:3rem;">
  <h1>🤖 Paxel - Chatbot de Karlito</h1>
  <p>Bot automatique WhatsApp connecté à Twilio.</p>
  <p><b>Status:</b> ✅ En ligne et prêt à répondre.</p>
</body>
</html>
