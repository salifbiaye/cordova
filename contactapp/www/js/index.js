/* Contact App — jQuery Mobile + cordova-plugin-contacts */

$(document).on('mobileinit', function () {
    $.mobile.defaultPageTransition = 'slide';
    $.mobile.ajaxEnabled = false;
});

document.addEventListener('deviceready', onDeviceReady, false);

function onDeviceReady() {
    App.init();
}

var App = (function ($) {

    /* ── Storage ── */
    var STORAGE_KEY = 'contactapp_contacts';

    var state = {
        contacts:   load(),
        group:      'all',
        search:     '',
        editingId:  null,
        deletingId: null
    };

    function load() {
        try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); }
        catch (_) { return []; }
    }

    function persist() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state.contacts));
    }

    /* ── Helpers ── */
    function esc(t) { return $('<div>').text(String(t || '')).html(); }

    function initials(name) {
        var parts = (name || '').trim().split(/\s+/);
        if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();
        return (parts[0] || '?').slice(0, 2).toUpperCase();
    }

    var GROUP_COLOR = {
        Famille: '#e74c3c',
        Amis:    '#2ecc71',
        Travail: '#3498db',
        Autre:   '#95a5a6'
    };

    /* ── cordova-plugin-contacts : importer depuis le téléphone ── */
    function importFromDevice() {
        if (!navigator.contacts) {
            setStatus('Plugin contacts non disponible');
            return;
        }
        var options = new ContactFindOptions();
        options.multiple = true;
        options.hasPhoneNumber = true;

        var fields = [
            navigator.contacts.fieldType.displayName,
            navigator.contacts.fieldType.name,
            navigator.contacts.fieldType.phoneNumbers,
            navigator.contacts.fieldType.emails
        ];

        navigator.contacts.find(fields, function (deviceContacts) {
            var added = 0;
            deviceContacts.forEach(function (dc) {
                var name  = dc.displayName || (dc.name && dc.name.formatted) || '';
                var phone = dc.phoneNumbers && dc.phoneNumbers.length ? dc.phoneNumbers[0].value : '';
                var email = dc.emails && dc.emails.length ? dc.emails[0].value : '';

                if (!name || !phone) return;

                // Eviter les doublons sur le numéro
                var exists = state.contacts.some(function (c) { return c.phone === phone.trim(); });
                if (!exists) {
                    state.contacts.push({
                        id:    Date.now() + Math.random(),
                        name:  name.trim(),
                        phone: phone.trim(),
                        email: email.trim(),
                        group: 'Autre'
                    });
                    added++;
                }
            });
            persist();
            render();
            setStatus(added + ' contact(s) importé(s)');
        }, function (err) {
            setStatus('Erreur import : ' + (err.message || err));
        });
    }

    /* ── Filtrage & tri ── */
    function getFiltered() {
        var q = state.search.toLowerCase();
        return state.contacts
            .filter(function (c) {
                var okGroup  = state.group === 'all' || c.group === state.group;
                var okSearch = !q || c.name.toLowerCase().indexOf(q) !== -1 || c.phone.indexOf(q) !== -1;
                return okGroup && okSearch;
            })
            .sort(function (a, b) { return a.name.localeCompare(b.name, 'fr'); });
    }

    /* ── Rendu liste ── */
    function buildItem(c) {
        var color = GROUP_COLOR[c.group] || GROUP_COLOR['Autre'];
        var avatar = '<span class="list-avatar" style="background:' + color + '">' + esc(initials(c.name)) + '</span>';
        return '<li data-id="' + c.id + '">' +
            '<a href="#page-detail" class="contact-link" data-id="' + c.id + '" data-transition="slide">' +
                avatar +
                '<h3>' + esc(c.name) + '</h3>' +
                '<p>' + esc(c.phone) + '</p>' +
                '<span class="ui-li-count">' + esc(c.group) + '</span>' +
            '</a>' +
        '</li>';
    }

    function renderList() {
        var filtered = getFiltered();
        var $list = $('#contact-list').empty();

        if (filtered.length === 0) {
            $list.append('<li><p style="text-align:center;padding:20px;">Aucun contact</p></li>');
        } else {
            filtered.forEach(function (c) { $list.append(buildItem(c)); });
        }

        // Refresh jQuery Mobile listview
        if ($list.data('mobile-listview')) {
            $list.listview('refresh');
        }
    }

    function renderSummary() {
        var n = state.contacts.length;
        $('#summary').text(n + ' contact' + (n > 1 ? 's' : ''));
    }

    function render() {
        renderList();
        renderSummary();
    }

    function setStatus(msg) {
        $('#footer-status').text(msg);
        setTimeout(function () { $('#footer-status').text('Prêt'); }, 3000);
    }

    /* ── Page détail ── */
    function showDetail(id) {
        var c = state.contacts.find(function (x) { return x.id === id; });
        if (!c) return;
        state.editingId = id;

        var color = GROUP_COLOR[c.group] || GROUP_COLOR['Autre'];
        var ini = initials(c.name);
        $('#detail-avatar').css('background', color);
        $('#detail-avatar-initials').text(ini);
        // Masquer l'image si on a des initiales, sinon afficher contact.png
        if (ini && ini !== '?') {
            $('#detail-avatar-img').hide();
            $('#detail-avatar-initials').show();
        } else {
            $('#detail-avatar-img').show();
            $('#detail-avatar-initials').hide();
        }

        var rows = [
            '<li data-role="list-divider">Informations</li>',
            '<li><a href="tel:' + esc(c.phone) + '"><h3>' + esc(c.name) + '</h3><p>Téléphone : ' + esc(c.phone) + '</p></a></li>'
        ];
        if (c.email) {
            rows.push('<li><a href="mailto:' + esc(c.email) + '"><p>Email : ' + esc(c.email) + '</p></a></li>');
        }
        rows.push('<li><p>Groupe : <strong>' + esc(c.group) + '</strong></p></li>');

        var $dl = $('#detail-list').html(rows.join(''));
        if ($dl.data('mobile-listview')) $dl.listview('refresh');
    }

    /* ── Formulaire ajout/modif ── */
    function openAdd() {
        state.editingId = null;
        $('#form-title').text('Nouveau contact');
        $('#f-id').val('');
        $('#f-name, #f-phone, #f-email').val('');
        $('#f-group').val('Autre').selectmenu && $('#f-group').selectmenu('refresh', true);
        $('#form-error').addClass('ui-helper-hidden');
    }

    function openEdit(id) {
        var c = state.contacts.find(function (x) { return x.id === id; });
        if (!c) return;
        state.editingId = id;
        $('#form-title').text('Modifier');
        $('#f-id').val(id);
        $('#f-name').val(c.name);
        $('#f-phone').val(c.phone);
        $('#f-email').val(c.email || '');
        $('#f-group').val(c.group);
        try { $('#f-group').selectmenu('refresh', true); } catch(e) {}
        $('#form-error').addClass('ui-helper-hidden');
        $.mobile.changePage('#page-add');
    }

    function saveContact() {
        var name  = $('#f-name').val().trim();
        var phone = $('#f-phone').val().trim();
        var email = $('#f-email').val().trim();
        var group = $('#f-group').val();
        var id    = $('#f-id').val();

        if (!name || !phone) {
            $('#form-error').removeClass('ui-helper-hidden');
            return;
        }

        if (id) {
            var existing = state.contacts.find(function (c) { return String(c.id) === String(id); });
            if (existing) { existing.name = name; existing.phone = phone; existing.email = email; existing.group = group; }
        } else {
            state.contacts.push({ id: Date.now(), name: name, phone: phone, email: email, group: group });
        }

        persist();
        render();
        setStatus('Contact enregistré');
        $.mobile.changePage('#page-list', { transition: 'slide', reverse: true });
    }

    /* ── Suppression ── */
    function askDelete(id) {
        state.deletingId = id;
        var c = state.contacts.find(function (x) { return x.id === id; });
        $('#confirm-msg').text('Supprimer "' + (c ? c.name : 'ce contact') + '" ?');
        $('#page-list').popup ? null : void 0;
        $('#popup-confirm').popup('open', { positionTo: 'window', transition: 'pop' });
    }

    function confirmDelete() {
        state.contacts = state.contacts.filter(function (c) { return c.id !== state.deletingId; });
        persist();
        render();
        state.deletingId = null;
        $('#popup-confirm').popup('close');
        $.mobile.changePage('#page-list', { transition: 'slide', reverse: true });
        setStatus('Contact supprimé');
    }

    /* ── Filtres ── */
    function setFilter(group) {
        state.group = group;
        $('.filter-btn').removeClass('ui-btn-active');
        $('.filter-btn[data-group="' + group + '"]').addClass('ui-btn-active');
        render();
    }

    /* ── Events ── */
    function bindEvents() {

        // Filtre groupe
        $(document).on('click', '.filter-btn', function (e) {
            e.preventDefault();
            setFilter($(this).data('group'));
        });

        // Recherche
        $(document).on('input', '#search-input', function () {
            state.search = $(this).val().trim();
            render();
        });

        // Clic sur un contact → page détail
        $(document).on('click', '.contact-link', function (e) {
            e.preventDefault();
            var id = +$(this).data('id');
            showDetail(id);
            $.mobile.changePage('#page-detail', { transition: 'slide' });
        });

        // Bouton Modifier dans détail
        $(document).on('click', '#btn-edit-detail', function (e) {
            e.preventDefault();
            openEdit(state.editingId);
        });

        // Bouton Supprimer dans détail
        $(document).on('click', '#btn-delete-detail', function (e) {
            e.preventDefault();
            askDelete(state.editingId);
        });

        // Popup confirmation suppression
        $(document).on('click', '#confirm-yes', function (e) {
            e.preventDefault();
            confirmDelete();
        });
        $(document).on('click', '#confirm-no', function (e) {
            e.preventDefault();
            $('#popup-confirm').popup('close');
        });

        // Enregistrer formulaire
        $(document).on('click', '#btn-save', function (e) {
            e.preventDefault();
            saveContact();
        });

        // Ouvrir formulaire vide depuis page-add
        $(document).on('pagebeforeshow', '#page-add', function () {
            if (!state.editingId) openAdd();
        });

        // Bouton import depuis téléphone (header page-list)
        $(document).on('click', '#btn-import', function (e) {
            e.preventDefault();
            importFromDevice();
        });
    }

    /* ── Init ── */
    function init() {
        // Ajouter bouton import dans le header après init JQM
        $(document).on('pagecreate', '#page-list', function () {
            $('[data-role="header"]', this).find('h1').after(
                '<a href="#" id="btn-import" data-icon="cloud" class="ui-btn-left" data-role="button">Importer</a>'
            );
            $('[data-role="header"]', this).trigger('create');
        });

        bindEvents();

        $(document).on('pageshow', '#page-list', function () {
            render();
        });
    }

    return { init: init };

}($));
