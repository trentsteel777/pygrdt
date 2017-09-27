var optionSearchWatchlistStore = Ext.create('Grdt.watchlist.Store', {
    storeId: 'optionSearchWatchlistStore',
    listeners : {
        load: function(thiz, records, successful, operation, eOpts ) {
            // On screen load default watchlist combobox to DEFAULT watchlist
            if(successful) {
                var optionSearchWatchlistComboBox = Ext.getCmp('optionSearchWatchlistComboBox');
                if(!optionSearchWatchlistComboBox.getValue()) {
                    var tickerIndex = thiz.find('name','DEFAULT');
                    optionSearchWatchlistComboBox.setValue(records[tickerIndex]);
                    Ext.data.StoreManager.lookup('optionSearchTickersStore').load(function(records, operation, success) {
                        optionSearchTickersComboBox.setValue(optionSearchTickersStore.getAt(0));
                    });
                }
                
            }
        }
    }
});

var optionSearchWatchlistComboBox = Ext.create('Grdt.watchlist.ComboBox', {
    id: 'optionSearchWatchlistComboBox',
    store: optionSearchWatchlistStore,
});



var optionSearchTickersStore = Ext.create('Grdt.ticker.Store', {
    storeId: 'optionSearchTickersStore',
     listeners: {
         beforeload: function(store, operation, eOpts) {
             operation._proxy.extraParams.watchlist = Ext.getCmp('optionSearchWatchlistComboBox').getValue();
         }
     }
});

var optionSearchTickersComboBox = Ext.create('Grdt.ticker.ComboBox', {
    id: 'optionSearchTickersComboBox',
    store: optionSearchTickersStore,
});

var optionSearchTimeComboBox = Ext.create('Grdt.time.ComboBox', {
    id: 'optionSearchTimeComboBox',
});

var datePicker = {
            xtype: 'datefield',
            fieldLabel: 'Date',
            name:'searchDate',
            labelAlign:'right',
            value: new Date(),
        };
        
var optionSearchButton = Ext.create('Ext.Button', {
    text: 'GO',
    handler: function() {
            Ext.data.StoreManager.lookup('optionSearchStore').load();
    }
});
 
 var optionSearchBar = Ext.create('Ext.form.Panel', {
    id: 'optionSearchBar',
    bodyPadding: 5, // Don't want content to crunch against the borders
    width: '100%',
    height: 40,
    url: PORTAL_URL,
    baseParams: {
        action: 'getOptionChain'
    },
    layout: 'hbox',
    //title: 'Search ',
    items: [
        optionSearchWatchlistComboBox,
        optionSearchTickersComboBox,
        datePicker,
        optionSearchTimeComboBox,
        {  
            xtype: 'tbspacer', width:15,
        },
        optionSearchButton,
        /*
            xtype: 'hiddenfield',
            name: 'start',
            value: '0'
        },
        {
            xtype: 'hiddenfield',
            name: 'limit',
            value: GRID_PAGE_SIZE
        }*/
    ],
});

 Ext.define('CallAndPutForStrike', {
     extend: 'Ext.data.Model',
     fields: [
        {name: 'callOptionType',   type: 'string'},
        {name: 'callExpiry',   type: 'string'},
        {name: 'callContractName', type: 'string'},
        {name: 'callLast',         type: 'number'},
        {name: 'callChange',       type: 'number'},
        {name: 'callBid',          type: 'number'},
        {name: 'callAsk',          type: 'number'},
        {name: 'callVolume',       type: 'int'},
        {name: 'callOpenInterest', type: 'number'},
        {name: 'callStrike',       type: 'number'},
        
        {name: 'putOptionType',   type: 'string'},
        {name: 'putExpiry',   type: 'string'},
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
 
 var optionSearchStore = Ext.create('Ext.data.Store', {
    storeId: 'optionSearchStore',
    model: 'CallAndPutForStrike',
    pageSize:GRID_PAGE_SIZE, // calls and puts get combined into one line per strike
     proxy: {
         type: 'ajax',
         url: PORTAL_URL,
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
            var formData = Ext.getCmp('optionSearchBar').getForm().getValues();
             Ext.apply(operation._proxy.extraParams, formData);
         }
     }
});

var optionSearchGrid = Ext.create('Ext.grid.Panel', {
    store:Ext.data.StoreManager.lookup('optionSearchStore'), 
    width: '100%',
    height: '100%',
    columns: [
        //{ text: 'optionType', dataIndex: 'callOptionType', flex:0.5 },
        { text: 'Calls', dataIndex: 'callExpiry', flex:0.6},
        //{ text: 'contractName', dataIndex: 'callContractName' , flex:0.5},
        { text: 'Last', dataIndex: 'callLast', flex:0.5 },
        { text: 'Change', dataIndex: 'callChange', flex:0.4 },
        { text: 'Bid', dataIndex: 'callBid' , flex:0.5},
        { text: 'Ask', dataIndex: 'callAsk' , flex:0.5},
        { text: 'Volume', dataIndex: 'callVolume' , flex:0.5},
        { text: 'Open Interest', dataIndex: 'callOpenInterest' , flex:0.5},
        { text: 'Strike', dataIndex: 'callStrike', flex:0.5 },
        
        //{ text: 'optionType', dataIndex: 'putOptionType', flex:0.5 },
        { text: 'Puts', dataIndex: 'putExpiry' , flex:0.6},
        //{ text: 'contractName', dataIndex: 'putContractName', flex:0.5 },
        { text: 'Last', dataIndex: 'putLast' , flex:0.5},
        { text: 'Change', dataIndex: 'putChange' , flex:0.4},
        { text: 'Bid', dataIndex: 'putBid' , flex:0.5},
        { text: 'Ask', dataIndex: 'putAsk' , flex:0.5},
        { text: 'Volume', dataIndex: 'putVolume', flex:0.5 },
        { text: 'Open Interest', dataIndex: 'putOpenInterest' , flex:0.5},
        // { text: 'strike', dataIndex: 'putStrike' , flex:0.5}, // already displayed by callStrike as they are the same
        
        
    ],
    tbar:optionSearchBar,
    bbar:Ext.create('Ext.PagingToolbar', {
        store: optionSearchStore,
        displayInfo: true,
        height:50,
        displayMsg: 'Displaying Calls and Puts {0} - {1} of {2}',
        emptyMsg: "No data to display"
    }),
});

var optionSearchPanel =  Ext.create('Ext.Panel', {
    title: 'Option Search',
    id :'optionSearchPanel',
    height: '100px',
    width: '50px',
    layout :'fit',
    items: [
        optionSearchGrid,
    ],
});