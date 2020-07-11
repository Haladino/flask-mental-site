const navigation = {

    button : document.querySelector( "#main_navigation--burger" ),
    menu   : document.querySelector( "#main_navigation--list_wrapper" ),

    open : function() {
        this.menu.classList.toggle( "open" );
        this.button.classList.toggle( "animate" );
    },

    close : function() {
        if ( this.menu.classList.contains( "open" ) ) this.menu.classList.remove( "open" ); this.button.classList.remove( "animate" );
    },

    init : function() {
        this.button.addEventListener( "click" , () => { this.open() } , false );
    },

}

window.onload = function() {
    navigation.init();
}
window.onresize = function() {
    if ( navigation.menu.classList.contains( "open" ) ) navigation.close();
}