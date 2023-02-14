$('a[rel=popover]').popover({
    html: true,
    content: function(){return '<img width="100%" src="'+$(this).data('img') + '" />';}
    });