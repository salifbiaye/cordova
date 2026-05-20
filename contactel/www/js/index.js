document.addEventListener('deviceready', function () {}, false);

var App = (function ($) {

    var STORAGE_KEY = 'contacts';

    var AVATAR_CLASS = {
        Famille: 'g-Famille',
        Amis:    'g-Amis',
        Travail: 'g-Travail',
        Autre:   'g-Autre'
    };

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

    function escape(text) {
        return $('<div>').text(String(text)).html();
    }

    function initials(name) {
        var parts = name.trim().split(/\s+/);
        return parts.length >= 2 ? parts[0][0] + parts[1][0] : parts[0].slice(0, 2);
    }

    function getFiltered() {
        return state.contacts
            .filter(function (c) {
                var matchGroup  = state.group === 'all' || c.group === state.group;
                var matchSearch = !state.search ||
                    c.name.toLowerCase().includes(state.search) ||
                    c.phone.includes(state.search);
                return matchGroup && matchSearch;
            })
            .sort(function (a, b) { return a.name.localeCompare(b.name, 'fr'); });
    }

    function buildContactHtml(c) {
        return '<li class="contact-item" data-id="' + c.id + '">' +
            '<div class="contact-avatar">' +
                '<img src="img/contact.png" class="avatar-img" alt="contact">' +
            '</div>' +
            '<div class="contact-info">' +
                '<div class="contact-name">'  + escape(c.name)  + '</div>' +
                '<div class="contact-phone">' + escape(c.phone) + '</div>' +
                '<span class="contact-group-badge">' + escape(c.group) + '</span>' +
            '</div>' +
            '<div class="contact-actions">' +
                '<button class="btn-edit"   data-id="' + c.id + '"><i class="fa-solid fa-pen"></i></button>' +
                '<button class="btn-delete" data-id="' + c.id + '"><i class="fa-solid fa-trash"></i></button>' +
            '</div>' +
        '</li>';
    }

    function renderList() {
        var filtered = getFiltered();
        var $list = $('#contact-list').empty();
        if (filtered.length === 0) {
            $list.append('<li id="empty-state"><div class="icon"><i class="fa-solid fa-address-book"></i></div><p>Aucun contact trouvé</p></li>');
        } else {
            filtered.forEach(function (c) { $list.append(buildContactHtml(c)); });
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

    function setFilter(group) {
        state.group = group;
        $('.filter-btn').removeClass('active');
        $('.filter-btn[data-group="' + group + '"]').addClass('active');
        render();
    }

    function setSearch(query) {
        state.search = query.trim().toLowerCase();
        render();
    }

    function openModal(id) {
        state.editingId = id;
        var c = id ? state.contacts.find(function (x) { return x.id === id; }) : null;

        $('#modal-title').text(c ? 'Modifier le contact' : 'Nouveau contact');
        $('#f-name').val(c ? c.name  : '');
        $('#f-phone').val(c ? c.phone : '');
        $('#f-email').val(c ? c.email : '');
        $('#f-group').val(c ? c.group : 'Autre');
        $('#form-error').addClass('hidden');
        updateAvatarPreview(c ? c.name : '');
        $('#modal-overlay').removeClass('hidden');
        setTimeout(function () { $('#f-name').focus(); }, 100);
    }

    function closeModal() {
        $('#modal-overlay').addClass('hidden');
        state.editingId = null;
    }

    function updateAvatarPreview(name) {
        var ini = name && name.trim() ? initials(name) : '';
        if (ini) {
            $('#avatar-preview-img').hide();
            $('#avatar-preview-initials').text(ini).show();
        } else {
            $('#avatar-preview-img').show();
            $('#avatar-preview-initials').hide();
        }
    }

    function readForm() {
        return {
            name:  $('#f-name').val().trim(),
            phone: $('#f-phone').val().trim(),
            email: $('#f-email').val().trim(),
            group: $('#f-group').val()
        };
    }

    function saveContact() {
        var data = readForm();
        if (!data.name || !data.phone) {
            $('#form-error').removeClass('hidden');
            return;
        }

        if (state.editingId) {
            var existing = state.contacts.find(function (c) { return c.id === state.editingId; });
            if (existing) Object.assign(existing, data);
        } else {
            state.contacts.push({ id: Date.now(), name: data.name, phone: data.phone, email: data.email, group: data.group });
        }

        persist();
        render();
        closeModal();
    }

    function askDelete(id) {
        state.deletingId = id;
        var c    = state.contacts.find(function (x) { return x.id === id; });
        var name = c ? c.name : 'ce contact';
        $('#confirm-msg').text('Supprimer "' + escape(name) + '" ?');
        $('#confirm-overlay').removeClass('hidden');
    }

    function cancelDelete() {
        $('#confirm-overlay').addClass('hidden');
        state.deletingId = null;
    }

    function confirmDelete() {
        state.contacts = state.contacts.filter(function (c) { return c.id !== state.deletingId; });
        persist();
        render();
        cancelDelete();
    }

    function bindEvents() {
        $('#btn-add').on('click', function () { openModal(null); });

        $(document).on('click', '.filter-btn', function () { setFilter($(this).data('group')); });

        $('#search-input').on('input', function () { setSearch($(this).val()); });

        $(document).on('click', '.btn-edit', function (e) {
            e.stopPropagation();
            openModal(+$(this).data('id'));
        });

        $(document).on('click', '.btn-delete', function (e) {
            e.stopPropagation();
            askDelete(+$(this).data('id'));
        });

        $('#f-name').on('input', function () { updateAvatarPreview($(this).val()); });

        $('#modal-close, #btn-cancel').on('click', closeModal);
        $('#modal-overlay').on('click', function (e) { if ($(e.target).is('#modal-overlay')) closeModal(); });

        $('#btn-save').on('click', saveContact);

        $('#confirm-no').on('click', cancelDelete);
        $('#confirm-overlay').on('click', function (e) { if ($(e.target).is('#confirm-overlay')) cancelDelete(); });
        $('#confirm-yes').on('click', confirmDelete);
    }

    function init() {
        bindEvents();
        render();
    }

    return { init: init };

}($));

$(App.init.bind(App));
