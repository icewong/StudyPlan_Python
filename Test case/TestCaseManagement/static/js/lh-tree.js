/*! liu_hui */

function tree_add_toggle_button(){
    var openedClass = 'glyphicon-minus';
    var closedClass = 'glyphicon-plus';

    var branch = $(this); //li with children ul
    var item = branch.prepend("<i class='indicator glyphicon " + closedClass + "'></i>")
    branch.addClass('branch');
    branch.children('i').eq(0).on('click', function (e) {
        if (this == e.target) {
            $(this).toggleClass(openedClass + " " + closedClass);
            $(this).parent('li').children().children().toggle();
        }
    });
    branch.children().children().toggle();
}


$.fn.extend({
    treed: function (o) {
        var openedClass = 'glyphicon-minus';
        var closedClass = 'glyphicon-plus';

        if (typeof o != 'undefined') {
            if (typeof o.openedClass != 'undefined') {
                openedClass = o.openedClass;
            }
            if (typeof o.closedClass != 'undefined') {
                closedClass = o.closedClass;
            }
        }

        //initialize each of the top levels
        var tree = $(this);
        tree.addClass("tree");
        tree.find('li').has("ul").each(tree_add_toggle_button);

        //fire event from the dynamically added icon
        tree.find('.branch .indicator').each(function () {
            $(this).on('click', function () {
                $(this).closest('li').click();
            });
        });
        //fire event to open branch if the li contains an anchor instead of text
        tree.find('.branch>a').each(function () {
            $(this).on('click', function (e) {
                $(this).closest('li').click();
                e.preventDefault();
            });
        });
        //fire event to open branch if the li contains a button instead of text
        tree.find('.branch>button').each(function () {
            $(this).on('click', function (e) {
                $(this).closest('li').click();
                e.preventDefault();
            });
        });
    },
    treed_checkbox: function (o) {
        var checkClass = 'glyphicon-check';
        var checkPartClass = 'glyphicon-stop';
        var uncheckClass = 'glyphicon-unchecked';

        var tree = $(this);
        tree.addClass("tree");
        tree.find('li').each(function () {
            var item = $(this);
            item.prepend("<i class='blank_space glyphicon " + uncheckClass + "'></i>");
            item.children('i').eq(0).on('click', function (e) {
                if (this == e.target) {
                    if ($(this).is('.'+checkPartClass)) {
                        $(this).removeClass(checkPartClass).addClass(checkClass);
                    }
                    else if ($(this).is('.'+checkClass)) {
                        $(this).removeClass(checkClass).addClass(uncheckClass);
                    }
                    else {
                        $(this).removeClass(uncheckClass).addClass(checkClass);
                    }
                    var st = $(this).is('.' + checkClass) ? [checkClass, uncheckClass] : [uncheckClass, checkClass];
                    $(this).nextAll().find('i.' + st[1] + ',i.' + checkPartClass).removeClass(st[1] + ' ' + checkPartClass).addClass(st[0]);
                    $(this).parents('ul').each(function () {
                            var unc = $(this).find('i.' + uncheckClass).length;
                            var c = $(this).find('i.' + checkClass).length;
                            if (c == 0) {
                                $(this).prevAll('i.' + checkPartClass + ',i.' + checkClass).removeClass(checkPartClass + ' ' + checkClass).addClass(uncheckClass)
                            }
                            else if (unc > 0) {
                                $(this).prevAll('i.' + uncheckClass + ',i.' + checkClass).removeClass(uncheckClass + ' ' + checkClass).addClass(checkPartClass)
                            }
                            else {
                                $(this).prevAll('i.' + checkPartClass + ',i.' + uncheckClass).removeClass(checkPartClass + ' ' + uncheckClass).addClass(checkClass)
                            }
                        }
                    );
                }
            })
        });

        var openedClass = 'glyphicon-minus';
        var closedClass = 'glyphicon-plus';

        tree.find('li').has("ul").each(function () {
            var branch = $(this); //li with children ul
            var item = branch.prepend("<i class='indicator glyphicon " + closedClass + "'></i>")
            branch.addClass('branch');
            branch.children('i').eq(0).on('click', function (e) {
                if (this == e.target) {
                    $(this).toggleClass(openedClass + " " + closedClass);
                    $(this).parent('li').children().children().toggle();
                }
            });
            branch.children().children().toggle();
        });
    }

});
