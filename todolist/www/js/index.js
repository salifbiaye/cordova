document.addEventListener('deviceready', function () {}, false);

var App = (function ($) {

    var STORAGE_KEY   = 'todos';
    var REVEAL_W      = 80;   // largeur du panel delete
    var SWIPE_COMMIT  = 60;   // px pour valider un swipe
    var DIR_THRESHOLD = 6;    // px avant de locker la direction

    var state = {
        tasks:     load(),
        filter:    'all',
        $open:     null   // item actuellement ouvert
    };

    /* ── Storage ── */
    function load() {
        try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); }
        catch (_) { return []; }
    }
    function persist() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state.tasks));
    }
    function escape(t) { return $('<div>').text(t).html(); }
    function plural(n) {
        return n + ' tâche' + (n > 1 ? 's' : '') + ' restante' + (n > 1 ? 's' : '');
    }

    /* ── Filtrage ── */
    function getFiltered() {
        return state.tasks.filter(function (t) {
            if (state.filter === 'active')    return !t.done;
            if (state.filter === 'completed') return t.done;
            return true;
        });
    }

    /* ── HTML ── */
    function buildTaskHtml(t) {
        return '<li class="task-item" data-id="' + t.id + '">' +
            /* Panel gauche : done (swipe droit) */
            '<div class="task-action-left">' +
                '<i class="fa-solid fa-check"></i>' +
            '</div>' +
            /* Panel droit : delete (swipe gauche) */
            '<div class="task-action-right">' +
                '<i class="fa-solid fa-trash"></i>' +
            '</div>' +
            /* Contenu (par dessus) */
            '<div class="task-content' + (t.done ? ' done' : '') + '">' +
                '<div class="task-check' + (t.done ? ' checked' : '') + '">' +
                    (t.done ? '<i class="fa-solid fa-check"></i>' : '') +
                '</div>' +
                '<span class="task-text">' + escape(t.text) + '</span>' +
            '</div>' +
        '</li>';
    }

    function buildEmptyHtml() {
        var cfg = {
            completed: { icon: 'fa-circle-check',   msg: 'Aucune tâche terminée' },
            active:    { icon: 'fa-hourglass-half', msg: 'Aucune tâche active' },
            all:       { icon: 'fa-list-check',     msg: 'Ajoutez votre première tâche !' }
        };
        var c = cfg[state.filter];
        return '<li id="empty-state">' +
            '<div class="icon"><i class="fa-solid ' + c.icon + '"></i></div>' +
            '<p>' + c.msg + '</p>' +
        '</li>';
    }

    /* ── Rendu ── */
    function renderList() {
        var filtered = getFiltered();
        var $list = $('#task-list').empty();
        closeOpen(false);
        if (filtered.length === 0) {
            $list.append(buildEmptyHtml());
        } else {
            filtered.forEach(function (t) { $list.append(buildTaskHtml(t)); });
        }
    }

    function renderSummary() {
        var n = state.tasks.filter(function (t) { return !t.done; }).length;
        $('#summary').text(plural(n));
    }

    function renderFooter() {
        $('#footer').toggle(state.tasks.some(function (t) { return t.done; }));
    }

    function render() { renderList(); renderSummary(); renderFooter(); }

    /* ── Actions ── */
    function addTask(text) {
        state.tasks.unshift({ id: Date.now(), text: text, done: false });
        persist(); render();
    }

    function toggleTask(id) {
        var t = state.tasks.find(function (t) { return t.id === id; });
        if (!t) return;
        t.done = !t.done;
        persist(); render();
    }

    function deleteTask(id, $item) {
        $item.addClass('anim-delete');
        setTimeout(function () {
            state.tasks = state.tasks.filter(function (t) { return t.id !== id; });
            persist(); render();
        }, 280);
    }

    function clearCompleted() {
        state.tasks = state.tasks.filter(function (t) { return !t.done; });
        persist(); render();
    }

    function setFilter(filter) {
        state.filter = filter;
        $('.filter-btn').removeClass('active');
        $('.filter-btn[data-filter="' + filter + '"]').addClass('active');
        render();
    }

    /* ── Swipe ── */
    function setTranslate($item, x, animate) {
        $item.find('.task-content').css({
            transition: animate ? 'transform 0.22s ease' : 'none',
            transform:  x ? 'translateX(' + x + 'px)' : ''
        });
        // Opacité du panel visible
        if (x > 0) {
            var pct = Math.min(x / REVEAL_W, 1);
            $item.find('.task-action-left').css('opacity', pct);
            $item.find('.task-action-right').css('opacity', 0);
        } else if (x < 0) {
            var pct2 = Math.min(-x / REVEAL_W, 1);
            $item.find('.task-action-right').css('opacity', pct2);
            $item.find('.task-action-left').css('opacity', 0);
        } else {
            $item.find('.task-action-left, .task-action-right').css('opacity', 0);
        }
    }

    function openItem($item) {
        if (state.$open && state.$open[0] !== $item[0]) closeOpen(true);
        state.$open = $item;
        $item.addClass('revealed');
        setTranslate($item, -REVEAL_W, true);
    }

    function closeOpen(animate) {
        if (!state.$open) return;
        setTranslate(state.$open, 0, animate);
        state.$open.removeClass('revealed');
        state.$open = null;
    }

    function bindSwipe() {
        var touch = { x: 0, y: 0, dir: null, active: false };

        $('#task-list').on('touchstart', '.task-item', function (e) {
            if ($(this).find('#empty-state').length) return;
            var t = e.originalEvent.touches[0];
            touch.x      = t.clientX;
            touch.y      = t.clientY;
            touch.dir    = null;
            touch.active = true;
            // Retirer transition pendant le drag
            $(this).find('.task-content').css('transition', 'none');
        });

        $('#task-list').on('touchmove', '.task-item', function (e) {
            if (!touch.active) return;
            var t  = e.originalEvent.touches[0];
            var dx = t.clientX - touch.x;
            var dy = t.clientY - touch.y;

            // Locker direction au premier mouvement significatif
            if (!touch.dir && Math.max(Math.abs(dx), Math.abs(dy)) > DIR_THRESHOLD) {
                touch.dir = Math.abs(dx) > Math.abs(dy) ? 'h' : 'v';
            }

            if (touch.dir !== 'h') return;
            e.preventDefault();

            var $item  = $(this);
            var isOpen = $item.hasClass('revealed');
            var base   = isOpen ? -REVEAL_W : 0;
            var raw    = base + dx;
            // Limites : gauche max -REVEAL_W-20, droite max +REVEAL_W
            var clamped = Math.min(REVEAL_W, Math.max(-(REVEAL_W + 20), raw));
            setTranslate($item, clamped, false);
        });

        $('#task-list').on('touchend', '.task-item', function (e) {
            if (!touch.active || touch.dir !== 'h') { touch.active = false; return; }
            touch.active = false;

            var t      = e.originalEvent.changedTouches[0];
            var dx     = t.clientX - touch.x;
            var $item  = $(this);
            var id     = +$item.data('id');
            var isOpen = $item.hasClass('revealed');

            if (!isOpen) {
                if (dx < -SWIPE_COMMIT) {
                    // Swipe gauche → ouvrir delete
                    openItem($item);
                } else if (dx > SWIPE_COMMIT) {
                    // Swipe droit → toggle done avec flash vert
                    setTranslate($item, 0, true);
                    $item.addClass('anim-done');
                    setTimeout(function () {
                        $item.removeClass('anim-done');
                        toggleTask(id);
                    }, 350);
                } else {
                    setTranslate($item, 0, true);
                }
            } else {
                if (dx > SWIPE_COMMIT / 2) {
                    closeOpen(true);
                } else if (dx < -SWIPE_COMMIT) {
                    // Swipe gauche complet → supprimer directement
                    deleteTask(id, $item);
                    state.$open = null;
                } else {
                    openItem($item);
                }
            }
        });

        // Tap sur le bouton delete révélé
        $('#task-list').on('click', '.task-action-right', function (e) {
            e.stopPropagation();
            var $item = $(this).closest('.task-item');
            deleteTask(+$item.data('id'), $item);
            state.$open = null;
        });

        // Tap ailleurs → fermer
        $(document).on('touchstart', function (e) {
            if (state.$open && !$(e.target).closest('.task-item').is(state.$open)) {
                closeOpen(true);
            }
        });
    }

    /* ── Modal ── */
    function openModal() {
        $('#f-task').val('');
        $('#form-error').addClass('hidden');
        $('#modal-overlay').removeClass('hidden');
        setTimeout(function () { $('#f-task').focus(); }, 150);
    }

    function closeModal() { $('#modal-overlay').addClass('hidden'); }

    function saveTask() {
        var text = $('#f-task').val().trim();
        if (!text) { $('#form-error').removeClass('hidden'); return; }
        addTask(text);
        closeModal();
    }

    /* ── Events ── */
    function bindEvents() {
        $('#btn-add').on('click', openModal);
        $('#modal-close, #btn-cancel').on('click', closeModal);
        $('#modal-overlay').on('click', function (e) {
            if ($(e.target).is('#modal-overlay')) closeModal();
        });
        $('#btn-save').on('click', saveTask);
        $('#f-task').on('keydown', function (e) { if (e.key === 'Enter') saveTask(); });

        // Tap checkbox ou texte
        $('#task-list').on('click', '.task-check, .task-text', function (e) {
            e.stopPropagation();
            if (state.$open) { closeOpen(true); return; }
            toggleTask(+$(this).closest('.task-item').data('id'));
        });

        $('.filter-btn').on('click', function () { setFilter($(this).data('filter')); });
        $('#btn-clear-completed').on('click', clearCompleted);

        bindSwipe();
    }

    function init() { bindEvents(); render(); }
    return { init: init };

}($));

$(App.init.bind(App));
