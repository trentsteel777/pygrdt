/* 
   Watchlist
*/
Ext.define('Grdt.model.Watchlist', {
     extend: 'Ext.data.Model',
     fields: [
        {name: 'watchlist',   type: 'string'},
     ]
 });

Ext.define('Grdt.watchlist.Store', {
    extend: 'Ext.data.Store',
    
    requires: ['Ext.data.Store'],
    
    model: 'Grdt.model.Watchlist',
    pageSize: GRID_PAGE_SIZE, // calls and puts get combined into one line per strike
     proxy: {
         type: 'ajax',
         url: PORTAL_URL,
         reader: {
             type: 'json',
             rootProperty: 'watchlists',
             totalProperty: 'watchlistsTotal',
         },
         extraParams: {
            action: 'getWatchlists'
        },
     },
     autoLoad: true,
     
});

Ext.define('Grdt.watchlist.ComboBox', {
    extend: 'Ext.form.ComboBox',
    
    requires: ['Ext.form.ComboBox'],
    
    fieldLabel: 'Watchlist',
    labelAlign:'right',
    queryMode: 'remote',
    name: 'watchlist',
    displayField: 'name',
    valueField: 'name',
});

/* 
   Ticker
*/

Ext.define('Grdt.model.Ticker', {
     extend: 'Ext.data.Model',
     fields: [
        {name: 'ticker',   type: 'string'},
     ]
});

Ext.define('Grdt.ticker.Store', {
    extend: 'Ext.data.Store',
    
    requires: ['Ext.data.Store'],
    
    model: 'Grdt.model.Ticker',
    pageSize:GRID_PAGE_SIZE, // calls and puts get combined into one line per strike
    proxy: {
        type: 'ajax',
        url: PORTAL_URL,
        reader: {
            type: 'json',
            rootProperty: 'tickers',
            totalProperty: 'tickersTotal',
        },
        extraParams: {
           action: 'getTickersByWatchlist',
        },
    },
    autoLoad: false,
});

Ext.define('Grdt.ticker.ComboBox', {
    extend: 'Ext.form.ComboBox',
    
    requires: ['Ext.form.ComboBox'],
    
    fieldLabel: 'Ticker',
    labelAlign:'right',
    queryMode: 'remote',
    name:'ticker',
    displayField: 'ticker',
    valueField: 'ticker',
});

/* 
   Time
*/

Ext.define('Grdt.time.ComboBox', {
    extend: 'Ext.form.ComboBox',
    
    requires: ['Ext.form.ComboBox', 'Ext.data.Store'],
    
    name:'hour',
    labelAlign:'right',
    fieldLabel: 'Hour',
    store: Ext.create('Ext.data.Store', {
        fields: ['hour'],
        data : [
            {"hour":"15",},
            {"hour":"16",},
            {"hour":"17",},
            {"hour":"18",},
            {"hour":"19",},
            {"hour":"20",},
            {"hour":"21",},
        ]
    }),
    queryMode: 'local',
    displayField: 'hour',
    
    initComponent : function(args) {
        this.callParent(args);
        this.on('afterrender', function(thiz) {
            var date = new Date();
            var currentHour = date.getHours();
            
            if( currentHour <= 21 && currentHour >= 3 ) {
                thiz.setValue(currentHour);
            }
            else if(currentHour > 21) {
                thiz.setValue('21');
            }
            else if(currentHour < 15) {
                thiz.setValue('15');
            }
            else {
                thiz.setValue(thiz.getStore().getAt(0));
            }
        });
    },
});

/* 
   OptionExpiry
*/

Ext.define('Grdt.model.OptionExpiry', {
     extend: 'Ext.data.Model',
     fields: [
        {name: 'expiry',   type: 'string'},
     ]
 });
 
Ext.define('Grdt.optionexpiry.Store', {
    extend: 'Ext.data.Store',
    
    requires: ['Ext.data.Store'],
    
    model: 'Grdt.model.OptionExpiry',
    pageSize: GRID_PAGE_SIZE, // calls and puts get combined into one line per strike
     proxy: {
         type: 'ajax',
         url: PORTAL_URL,
         reader: {
             type: 'json',
             rootProperty: 'expiryList',
             totalProperty: 'expiryListTotal',
         },
         extraParams: {
            action: 'optionExpiriesList'
        },
     },
    autoLoad: false,
     
});

Ext.define('Grdt.optionexpiry.ComboBox', {
    extend: 'Ext.form.ComboBox',
    
    requires: ['Ext.form.ComboBox'],
    
    fieldLabel: 'Expiry',
    labelAlign:'right',
    queryMode: 'remote',
    name: 'expiry',
    displayField: 'expiry',
    valueField: 'expiry',
});

