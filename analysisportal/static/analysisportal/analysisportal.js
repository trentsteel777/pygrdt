Ext.onReady(function() {
  buildUi();
});
function buildUi() {
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
            layout: 'fit',
            width: 150,
            items:[
                navigationTreePanel,
            ]
            
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
            xtype: 'panel', // TabPanel itself has no title
            layout:'fit',
            id:'mainView',
             items:[   
               optionSearchPanel
            ]

        }]
    });
}
var navigationStore = Ext.create('Ext.data.TreeStore', {
    root: {
        expanded: true,
        children: [
            { text: 'Option Search', leaf: true, view: 'optionSearchPanel' },
            { text: 'Strategies', expanded: true, children: [
                { text: 'Jerry Lee', leaf: true , view: 'jerryLeePanel'},
                //{ text: 'algebra', leaf: true}
            ] },
            //{ text: 'buy lottery tickets', leaf: true }
        ]
    }
});

function navigationHandler(view) {
    if(view) {
      var mainView = Ext.getCmp('mainView');
      var childItemIndex = 0;
      var doDestroy = false;
      mainView.remove(childItemIndex, doDestroy);
      mainView.add(view);
    }
}

var navigationTreePanel = Ext.create('Ext.tree.Panel', {
    //title: 'Simple Tree',
    id:'navigationTreePanel',
    width: 200,
    height: 200,
    store: navigationStore,
    rootVisible: false,
    listeners: {
        itemclick: function(thiz, record) {
            var view = record.data.view;
            navigationHandler(view);
        }
    }
});










