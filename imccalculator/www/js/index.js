document.addEventListener('deviceready', function () {}, false);

var App = (function () {

    var RING_MAX = 40;
    var RING_LEN = 314;

    var CATEGORIES = [
        { max: 18.5, label: 'Insuffisance pondérale', advice: 'Votre poids est inférieur à la normale. Consultez un professionnel de santé.', color: '#ffb443' },
        { max: 25,   label: 'Poids normal',            advice: 'Votre poids est dans la plage santé. Continuez vos bonnes habitudes !',        color: '#00e87a' },
        { max: 30,   label: 'Surpoids',                advice: 'Un léger excès de poids. Une activité physique régulière peut aider.',          color: '#ffb443' },
        { max: 35,   label: 'Obésité modérée',         advice: 'Un suivi médical est recommandé pour votre santé.',                             color: '#ff7043' },
        { max: Infinity, label: 'Obésité sévère',      advice: 'Consultez rapidement un professionnel de santé.',                               color: '#ff4d6a' }
    ];

    function getCategory(imc) {
        return CATEGORIES.find(function (c) { return imc < c.max; });
    }

    function validate(masse, taille) {
        var errors = [];
        if (!masse || masse < 1 || masse > 500) errors.push('masse');
        if (!taille || taille < 0.5 || taille > 3) errors.push('taille');
        return errors;
    }

    function showErrors(fields) {
        document.getElementById('masse').classList.remove('error');
        document.getElementById('taille').classList.remove('error');
        fields.forEach(function (id) {
            document.getElementById(id).classList.add('error');
        });
    }

    function animateRing(imc, color) {
        var fill   = document.querySelector('.ring-fill');
        var offset = RING_LEN * (1 - Math.min(imc / RING_MAX, 1));
        fill.style.stroke = color;
        setTimeout(function () { fill.style.strokeDashoffset = offset; }, 50);
    }

    function showResult(imc, category) {
        document.getElementById('result-value').textContent    = Math.round(imc * 10) / 10;
        document.getElementById('result-category').textContent = category.label;
        document.getElementById('result-category').style.color = category.color;
        document.getElementById('result-advice').textContent   = category.advice;

        var resultDiv = document.getElementById('result');
        resultDiv.removeAttribute('hidden');
        resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function onSubmit(e) {
        e.preventDefault();

        var masse  = parseFloat(document.getElementById('masse').value);
        var taille = parseFloat(document.getElementById('taille').value);
        var errors = validate(masse, taille);

        showErrors(errors);
        if (errors.length) return;

        var imc      = masse / (taille * taille);
        var category = getCategory(imc);

        showResult(imc, category);
        animateRing(imc, category.color);
    }

    function bindEvents() {
        document.getElementById('imc-form').addEventListener('submit', onSubmit);
    }

    function init() {
        bindEvents();
    }

    return { init: init };

}());

App.init();
