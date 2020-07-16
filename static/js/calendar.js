(function() {

    class bookingApp {

        constructor() {
            this.form = document.getElementById( 'booking_form' );
            this.data = {};
            this.UI = new UI( this );
            this.module = new module( this );


            this.UI.pages.forEach( p => {
                p.label.addEventListener( 'click' , (e) => {
                    this.UI.togglePages( e.target );
                }, false);
            });
            this.UI.closePages();
            this.UI.openPage( 0 );


            const details = this.module.createStage( 'details' );
            details.setValidation( 'form', document.querySelectorAll('input') );
            details.onError = function() {
                // details.stageError
                console.log( details.stageError );
            }
            details.setFunction(
                () => {

                },
                this.UI.pages[0]
            );
            
            const calendar = this.module.createStage( 'calendar' );
            calendar.setValidation( 'calendar' );
            calendar.onError = function() {

            }
            calendar.setFunction(
                () => {
                    // get available dates
                },
                this.UI.pages[1]
            );

            const checkout = this.module.createStage( 'checkout' );
            checkout.onError = function() {
                // Ajax error response
            }
            checkout.setFunction(
                () => {
                    // send form
                    // Ajax request
                },
                this.UI.pages[2]
            );
            
            details.setNextStage( calendar );
            calendar.setNextStage( checkout );

            this.module.run();

        }



    }


    class module {
        constructor( application ) {
            this.application = application;
            this.stages = {}
            this.currentStage = 1;
            this.currentStageID = undefined;
            this.length = 0;
        
            this.application.UI.stepButtons.forEach( btn => {
                if( btn.classList.contains( 'button_forward' ) )
                {
                    btn.addEventListener( 'click' , (e) => { 
                        this.update(); 
                    } , false );
                }
            });
        }

        run()
        {
            for( let key in this.stages )
            {
                if( this.stages[ key ].stageIndex != 0 ) this.stages[ key ].lockStage();
            }

            this.setProgressStage( this.currentStage );
        }

        update()
        {
            for( let key in this.stages )
            {
                if( this.stages[ key ].isLocked == false && this.stages[ key ].isValid == false  ) 
                {
                    let result = this.stages[ key ].validateStage();

                    if( typeof(result) == 'boolean' && result )
                    {
                        if( this.stages[ key ].nextStage && this.stages[ key ].nextStage.isLocked )
                        {
                            this.unlockNextStage( key );
                            this.setProgressStage( this.stages[ key ].nextStage.stageIndex + 1);
                        
                        } else {

                            this.stages[ key ].run();
                        }

                    }

                    if( typeof(result) == 'object' )
                    {
                        //  Meaning the Validation is False and returns errors
                    }
                    
                }
            }

        }


        unlockNextStage( key )
        {
            this.stages[ key ].nextStage.unlockStage();
            this.stages[ key ].stagePage.close();
            this.stages[ key ].nextStage.stagePage.open();

            this.application.UI.findOpenedPage();
        }


        setProgressStage( stage )
        {
            this.application.UI.progressBar.classList.remove( 'stage_' + this.currentStage.toString() )
            this.application.UI.progressBar.classList.add( 'stage_' + stage.toString() );
            this.currentStage = stage;
        }

        createStage( stageID )
        {
            this.stages[ stageID ] = new stage( this.application , stageID );
            this.stages[ stageID ].stageIndex = this.length;
            this.setNumberOfStages();

            return this.stages[ stageID ];
        }

        setNumberOfStages()
        {
            this.length++;
        }

        getNumberOfStages()
        {
            return this.length;
        }

    }


    class stage {
        constructor( application, stageID ) {
            this.application = application;
            this.stageID = stageID;
            this.stagePage = {};
            this.isLocked = false;
            this.validation = undefined;
            this.isValid = false;
            this.stageFunction = undefined;
            this.nextStage = {};
            this.stageError = null;
            this.onError = undefined;
        }

        run()
        {
            this.stageFunction();
        }

        validateStage()
        {
            this.resetStage();

            if ( this.validation != undefined ) 
            {
                let result = this.validation.run();

                if( typeof(result) == 'object' )
                {
                    this.isValid = false;
                    this.stageError = result;

                    if ( this.onError && typeof(this.onError) == 'function' ) this.onError();
                
                } else {
                    this.isValid = true;
                }

                return result;
            }
        }

        setValidation( validationType, validateThis )
        {
            if( this.validation == undefined )
            {
                this.validation = new validation( this, validationType , validateThis );
            
            } else {
             
                this.validation.setTo( validationType , validateThis );
            }
        }

        resetStage()
        {
            this.isValid = false;
            this.stageError = null;
        }

        lockStage()
        {
            if( !this.isLocked )
            {
                this.isLocked = true;
                this.stagePage.block();
            }
        }

        unlockStage()
        {
            if( this.isLocked )
            {
                this.isLocked = false;
                this.stagePage.unblock();
            }
        }

        setNextStage( object )
        {
            this.nextStage = object;
        }

        setFunction( doThis, thisPage )
        {
            this.stageFunction = doThis;
            this.stagePage = thisPage;
        }

        setOnError( callback )
        {
            this.onError = callback;
        }

        getStageID()
        {
            return this.stageID;
        }

    }


    class validation {
        constructor( stage, validationType, objectNeedsValidating ) {
            this.stage = stage;
            this.validationType = undefined;
            this.validation = undefined;
            this.objectNeedsValidating = objectNeedsValidating;
            this.result = undefined;

            this.setTo( validationType );

        }

        run() {
            if( this.validation != undefined && typeof(this.validation) == 'function' )
            {
                this.result = this.validation( this.objectNeedsValidating || [] );
                return this.result;
            }
        }

        setTo( validationType , autoRun = false )
        {
            const types = {
                form : function( inputs ) 
                {
                    let result = true;
                    let checks = {};

                    inputs.forEach( input => {
                        
                        switch( input.type )
                        {
                            case 'text'  : checks[input.name] = this.validateText( input.value || input.textContent ); break;
                            case 'tel'   : checks[input.name] = this.validateTel( input.value || input.textContent ); break;
                            case 'email' : checks[input.name] = this.validateEmail( input.value || input.textContent ); break;
                            default      : checks[input.name] = this.validateString( input.value || input.textContent );
                        }
                    });

                    for( let key in checks )
                    {
                        if( checks[ key ] != true ) 
                        {
                            if( typeof(result) !== 'object' ) result = {};

                            result[key + 'Error'] = checks[ key ];
                        }
                    }

                    return result;   // Gonna be true or False
                },
                calendar : function() {
                    return false;
                }
            }

            this.validationType = validationType;
            this.validation = types[ validationType ];
            
            if( autoRun ) return this.run();

        }

        validateText( input )
        {
            let string = input.trim();

            if( string == '' || string == ' ') return 'Field cant be empty';
            
            let regExp = new RegExp('[^A-Za-z\-\_ áéíóöőúüűÁÉÍÓÖŐÜÚŰ]');

            if ( regExp.test( string ) )
            {
                return 'invalid text';
            }

            return true;
        }

        validateTel( input )
        {
            let number = input.trim();
            let regExp = new RegExp('[^0-9\-\/]');

            if ( Number.isNaN( number ) ) return 'Not a number';
            if ( regExp.test( number ) ) return 'Invalid characters';

            return true;
        }

        validateEmail( input )
        {
            return true;
        }

        validateString( input )
        {
            return true;
        }
    }



    class UI {

        constructor( application ) {
            this.application = application;
            this.pages = [];
            this.openedPage = {};
            this.stepButtons = document.querySelectorAll( '.step_button' );
            this.progressBar = document.getElementById( 'progress' );

            const labels = document.getElementsByClassName( 'booking_form_button' );
            const bodies = document.getElementsByClassName( 'booking_form_page');
            const info_block = document.getElementById( 'info_block' );

            for ( let i = 0; i < labels.length; i ++ )
            {
                this.pages.push( new page( labels[ i ] , bodies[ i ] ) );
            }

            this.pages.forEach( p => {
                p.label.addEventListener( 'click' , (e) => {
                    e.preventDefault();
                    this.togglePages( e.target );
                }, false);
            });

            this.stepButtons.forEach( sb => {
                sb.addEventListener( "click" , (e) => {
                    e.preventDefault();
                    this.togglePages( e.target )
                }, false);
            });

            info_block.classList.add( 'hidden' );
            info_block.addEventListener( 'click' , (e) => {
                e.target.classList.remove( 'hidden' );
            }, false);
        }


        togglePages( target )
        {
            if ( !this.pages[ target.getAttribute( 'data-pointsTo') ].isBlocked )
            {
                this.closeOpenedPage();
                this.openPage( target.getAttribute( 'data-pointsTo' ) );
            }
        }


        findOpenedPage()
        {
            this.pages.forEach( p => {
                if( p.isOpen ) this.openedPage = p; return this.openedPage;   
            });
        }


        openPage( index )
        {
            if ( !this.pages[ index ].isBlocked )
            {
                this.openedPage = this.pages[ index ].open();
            }

        }


        closeOpenedPage()
        {
            this.openedPage.close();
        }


        closePages() 
        {
            this.pages.forEach(page => {
                page.close();
            });
        }

    }



    class page {
        constructor( label , body ) {
            this.id     = Math.round( Math.random() * 100 );
            this.label  = label;
            this.body   = body;
            this.isOpen = false;
            this.isBlocked = false;
        }

        block() {
            this.label.classList.add( 'blocked' );
            this.isBlocked = true;
        }

        unblock() {
            this.label.classList.remove( 'blocked' );
            this.isBlocked = false;
        }

        open() {
            this.label.classList.add( 'active' );
            this.body.style.display = "block";
            this.isOpen = true;

            return this;
        }

        close() {
            this.label.classList.remove( 'active' );
            this.body.style.display = "none";
            this.isOpen = false;
        }

    }





    const main = (function() {

        const app = new bookingApp();
        // app.UI.closePages();
        // console.log( document.querySelectorAll('input'));
        // console.log(app.UI);

    })();



})();