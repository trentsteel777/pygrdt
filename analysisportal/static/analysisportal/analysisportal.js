var portalUrl = 'ajax/dispatcher/';
var gridPageSize = 25;
Ext.onReady(function() {
    Ext.create('Ext.container.Viewport', {
        layout: 'border',
        items: [{
            region: 'north',
            html: '<h1 class="x-panel-header">Page Title</h1>',
            border: false,
            margin: '0 0 5 0'
        }, {
            region: 'west',
            collapsible: true,
            title: 'Navigation',
            width: 150
                // could use a TreePanel or AccordionLayout for navigational items
        }, {
            region: 'south',
            title: 'South Panel',
            collapsible: true,
            html: 'Information goes here',
            split: true,
            height: 100,
            minHeight: 100
        }, {
            region: 'east',
            title: 'East Panel',
            collapsible: true,
            split: true,
            width: 150
        }, {
            region: 'center',
            xtype: 'tabpanel', // TabPanel itself has no title
            activeTab: 0, // First tab active by default
             items:[   
                {
                    title: 'Optionchain Search',
                    height: '100px',
                    width: '50px',
                    layout :'fit',
                    items: [
                        grid,
                    ],
                },
            ]

        }]
    });

});

Ext.define('Watchlist', {
     extend: 'Ext.data.Model',
     fields: [
        {name: 'watchlist',   type: 'string'},
     ]
 });
 var watchlistStore = Ext.create('Ext.data.Store', {
    storeId: 'watchlistStore',
    model: 'Watchlist',
    pageSize:gridPageSize, // calls and puts get combined into one line per strike
     proxy: {
         type: 'ajax',
         url: portalUrl,
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
     listeners : {
        load: function(thiz, records, successful, operation, eOpts ) {
            // On screen load default watchlist combobox to DEFAULT watchlist
            if(successful) {
                var watchlistComboBox = Ext.getCmp('watchlistComboBox');
                if(!watchlistComboBox.getValue()) {
                    var tickerIndex = thiz.find('name','DEFAULT');
                    watchlistComboBox.setValue(records[tickerIndex]);
                    Ext.data.StoreManager.lookup('tickersStore').load(function(records, operation, success) {
                        tickersComboBox.setValue(tickersStore.getAt(0));
                    });
                }
                
            }
        }
    }
});

var watchlistComboBox = Ext.create('Ext.form.ComboBox', {
    id: 'watchlistComboBox',
    fieldLabel: 'Watchlist',
    labelAlign:'right',
    store: watchlistStore,
    queryMode: 'remote',
    name: 'watchlist',
    displayField: 'name',
    valueField: 'name',
});

Ext.define('Ticker', {
     extend: 'Ext.data.Model',
     fields: [
        {name: 'ticker',   type: 'string'},
     ]
});
var tickersStore = Ext.create('Ext.data.Store', {
    storeId: 'tickersStore',
    model: 'Ticker',
    pageSize:gridPageSize, // calls and puts get combined into one line per strike
     proxy: {
         type: 'ajax',
         url: portalUrl,
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
     listeners: {
         beforeload: function(store, operation, eOpts) {
             operation._proxy.extraParams.watchlist = Ext.getCmp('watchlistComboBox').getValue();
         }
     }
});
var tickersComboBox = Ext.create('Ext.form.ComboBox', {
    id: 'tickersComboBox',
    fieldLabel: 'Ticker',
    labelAlign:'right',
    store: tickersStore,
    queryMode: 'remote',
    name:'ticker',
    displayField: 'ticker',
    valueField: 'ticker',
});

var timeComboBox = Ext.create('Ext.form.ComboBox', {
    id: 'timeComboBox',
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
    listeners: {
        afterrender: function(thiz) {
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
        }            
    }
});
var datePicker = {
            xtype: 'datefield',
            fieldLabel: 'Date',
            name:'searchDate',
            labelAlign:'right',
            value: new Date(),
        };
        
var searchButton = Ext.create('Ext.Button', {
    text: 'GO',
    handler: function() {
            Ext.data.StoreManager.lookup('optionStore').load();
    }
});

var searchBar = Ext.create('Ext.form.Panel', {
    id: 'searchBar',
    bodyPadding: 5, // Don't want content to crunch against the borders
    width: '100%',
    height: 40,
    url: portalUrl,
    baseParams: {
        action: 'getOptionChain'
    },
    layout: 'hbox',
    //title: 'Search ',
    items: [
        watchlistComboBox,
        tickersComboBox,
        datePicker,
        timeComboBox,
        {  
            xtype: 'tbspacer', width:15,
        },
        searchButton,
        /*
            xtype: 'hiddenfield',
            name: 'start',
            value: '0'
        },
        {
            xtype: 'hiddenfield',
            name: 'limit',
            value: gridPageSize
        }*/
    ],
});

 Ext.define('CallAndPutForStrike', {
     extend: 'Ext.data.Model',
     fields: [
        {name: 'callOptionType',   type: 'string'},
        {name: 'callNasdaqName',   type: 'string'},
        {name: 'callContractName', type: 'string'},
        {name: 'callLast',         type: 'number'},
        {name: 'callChange',       type: 'number'},
        {name: 'callBid',          type: 'number'},
        {name: 'callAsk',          type: 'number'},
        {name: 'callVolume',       type: 'int'},
        {name: 'callOpenInterest', type: 'number'},
        {name: 'callStrike',       type: 'number'},
        
        {name: 'putOptionType',   type: 'string'},
        {name: 'putNasdaqName',   type: 'string'},
        {name: 'putContractName', type: 'string'},
        {name: 'putLast',         type: 'number'},
        {name: 'putChange',       type: 'number'},
        {name: 'putBid',          type: 'number'},
        {name: 'putAsk',          type: 'number'},
        {name: 'putVolume',       type: 'int'},
        {name: 'putOpenInterest', type: 'number'},
        {name: 'putStrike',       type: 'number'},
     ]
 });
 
 var optionStore = Ext.create('Ext.data.Store', {
    storeId: 'optionStore',
    model: 'CallAndPutForStrike',
    pageSize:gridPageSize, // calls and puts get combined into one line per strike
     proxy: {
         type: 'ajax',
         url: portalUrl,
         reader: {
             type: 'json',
             rootProperty: 'optionChain',
             totalProperty: 'optionTotal',
         },
         extraParams: {
            action: 'getOptionChain'
        },
     },
     autoLoad: false,
     listeners: {
         beforeload: function(store, operation, eOpts) {
            var formData = Ext.getCmp('searchBar').getForm().getValues();
             Ext.apply(operation._proxy.extraParams, formData);
         }
     }
});

var grid = Ext.create('Ext.grid.Panel', {
    store:Ext.data.StoreManager.lookup('optionStore'), 
    width: '100%',
    height: '100%',
    columns: [
        //{ text: 'optionType', dataIndex: 'callOptionType', flex:0.5 },
        { text: 'Calls', dataIndex: 'callNasdaqName', flex:0.6},
        //{ text: 'contractName', dataIndex: 'callContractName' , flex:0.5},
        { text: 'Last', dataIndex: 'callLast', flex:0.5 },
        { text: 'Change', dataIndex: 'callChange', flex:0.4 },
        { text: 'Bid', dataIndex: 'callBid' , flex:0.5},
        { text: 'Ask', dataIndex: 'callAsk' , flex:0.5},
        { text: 'Volume', dataIndex: 'callVolume' , flex:0.5},
        { text: 'Open Interest', dataIndex: 'callOpenInterest' , flex:0.5},
        { text: 'Strike', dataIndex: 'callStrike', flex:0.5 },
        
        //{ text: 'optionType', dataIndex: 'putOptionType', flex:0.5 },
        { text: 'Puts', dataIndex: 'putNasdaqName' , flex:0.6},
        //{ text: 'contractName', dataIndex: 'putContractName', flex:0.5 },
        { text: 'Last', dataIndex: 'putLast' , flex:0.5},
        { text: 'Change', dataIndex: 'putChange' , flex:0.4},
        { text: 'Bid', dataIndex: 'putBid' , flex:0.5},
        { text: 'Ask', dataIndex: 'putAsk' , flex:0.5},
        { text: 'Volume', dataIndex: 'putVolume', flex:0.5 },
        { text: 'Open Interest', dataIndex: 'putOpenInterest' , flex:0.5},
        // { text: 'strike', dataIndex: 'putStrike' , flex:0.5}, // already displayed by callStrike as they are the same
        
        
    ],
    tbar:searchBar,
    bbar:Ext.create('Ext.PagingToolbar', {
        store: optionStore,
        displayInfo: true,
        height:50,
        displayMsg: 'Displaying Calls and Puts {0} - {1} of {2}',
        emptyMsg: "No data to display"
    }),
});

