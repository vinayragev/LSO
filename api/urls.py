from django.urls import path,include
from .controller.home import home
from .controller.user import user
from .controller.category import category
from .controller.sign import sign
from .controller.product import product
from .controller.service import service
from .controller.service_price import service_price
from .controller.admin import admin
from .controller.shop import shop
from .controller.file import file
from .controller.product_price import product_price
from .controller.label import label
from .controller.order import order
from .controller.query import query


urlpatterns = [
    # path('',                            home.index             ),
    path('search',              home.search),

    # path('product_detail',      home.product_detail),     
    # path('shop',                home.shop),               
    # path('add_to_cart',         home.add_to_cart),        
    # path('remove_from_cart',    home.remove_from_cart),   
    # path('user_book_now',       home.user_book_now),      
    # path('service_detail',      home.service_detail),     
    # path('product_shop_list',   home.product_shop_list),  
    # path('service_shop_list',   home.service_shop_list),  
    # path('seller_product',      home.seller_product),     
    # path('seller_service',      home.seller_service),     
    # path('seller_cart_list',    home.seller_cart_list),   
    # path('seller_order_list',   home.seller_order_list),  
    # path('seller_detail',       home.seller_detail),      
    # path('change_cart_status',  home.change_cart_status), 
    # path('user_send_query',     home.user_send_query),    
    # path('user_profile_detail', home.user_profile_detail),
    # path('user_profile_update', home.user_profile_update),
    # path('user_order_list',     home.user_order_list),    
    # path('user_query_list',     home.user_query_list),    
    # path('user_cart_list',      home.user_cart_list),     
    # path('user_order_token',    home.user_order_token),   
    # path('user_add_review',     home.user_add_review),    
    # path('user_order_detail',   home.user_order_detail),  
    # path('user_query_detail',   home.user_query_detail),  
    # path('user_query_replay',   home.user_query_replay),  

    path('shop'                 ,home.shop),
    path('search'               ,home.search),
    path('add_to_cart'          ,home.add_to_cart),
    path('remove_from_cart'     ,home.remove_from_cart),
    path('search_filter_select' ,home.search_filter_select),
    path('user_book_now'        ,home.user_book_now),
    path('user_send_query'      ,home.user_send_query),
    path('product_detail'       ,home.product_detail),
    path('product_shop_list'    ,home.product_shop_list),
    path('service_detail'       ,home.service_detail),
    path('service_shop_list'    ,home.service_shop_list),
    path('seller_product'       ,home.seller_product),
    path('seller_service'       ,home.seller_service),
    path('seller_cart_list'     ,home.seller_cart_list),
    path('seller_order_list'    ,home.seller_order_list),
    path('seller_detail'        ,home.seller_detail),
    path('change_cart_status'   ,home.change_cart_status),
    path('user_profile_detail'  ,home.user_profile_detail),
    path('user_profile_update'  ,home.user_profile_update),
    path('user_order_list'      ,home.user_order_list),
    path('user_query_list'      ,home.user_query_list),
    path('user_address_list'    ,home.user_address_list),
    path('user_address_add'     ,home.user_address_add),
    path('user_address_edit'    ,home.user_address_edit),
    path('user_address_delete'  ,home.user_address_delete),
    path('user_cart_list'       ,home.user_cart_list),
    path('user_add_review'      ,home.user_add_review),
    path('user_order_token'     ,home.user_order_token),
    path('user_order_detail'    ,home.user_order_detail),
    path('user_query_replay'    ,home.user_query_replay),
    path('user_query_detail'    ,home.user_query_detail),


    # path('search',                      home.search            ),
    # path('shop',                        home.shop              ),
    # path('product',                     home.product           ),
    # path('service',                     home.service           ),
    # # path('geolocation',                 home.geolocation       ),
    # path('seller',                      home.seller            ),
    # path('order',                       home.order             ),
    # path('profile',                     home.profile           ),
    # path('profile/edit',                home.profile_edit      ),
    # path('order_detail',                home.order_detail      ),
    # path('query_detail',                home.query_detail      ),
    # # path('add_staff',                   home.add_staff         ),

    path('signup',                      sign._up               ),
    path('signin',                      sign._in               ),
    path('signout',                     sign._out              ),
    path('admin/',                      admin.dashboard        ),
    path('admin/profile',               admin.profile          ),
    path('admin/profile/edit',          admin.profile_edit     ),

    path('admin/file/upload',           file.upload            ),
    path('admin/file/remove',           file.remove            ),
    
    path('admin/category/add',          category.add           ),
    path('admin/category/list',         category.list          ),
    path('admin/category/edit',         category.edit          ),
    path('admin/category/view',         category.view          ),
    path('admin/category/form',         category.form          ),
    path('admin/category/search',       category.search        ),
    path('admin/category/delete',       category.delete        ),
    
    path('admin/product/add',           product.add            ),
    path('admin/product/list',          product.list           ),
    path('admin/product/view',          product.view           ),
    path('admin/product/form',          product.form           ),
    path('admin/product/edit',          product.edit           ),
    path('admin/product/remove_photo',          product.remove_photo           ),
    path('admin/product/delete',        product.delete         ),

    path('admin/product/price/add',     product_price.add      ),
    path('admin/product/price/list',    product_price.list     ),
    path('admin/product/price/table',   product_price.table    ),
    path('admin/product/price/edit',    product_price.edit     ),
    path('admin/product/price/view',    product_price.view     ),
    path('admin/product/price/form',    product_price.form     ),
    path('admin/product/price/delete',  product_price.delete   ),

    path('admin/service/add',           service.add            ),
    path('admin/service/list',          service.list           ),
    path('admin/service/edit',          service.edit           ),
    # path('admin/service/view',          service.view           ),
    path('admin/service/form',          service.form           ),
    path('admin/service/delete',        service.delete         ),

    path('admin/service/price/add',     service_price.add      ),
    path('admin/service/price/list',    service_price.list     ),
    path('admin/service/price/table',   service_price.table    ),
    path('admin/service/price/edit',    service_price.edit     ),
    path('admin/service/price/form',    service_price.form     ),
    path('admin/service/price/delete',  service_price.delete   ),

    path('admin/shop/add',              shop.add               ),
    path('admin/shop/list',             shop.list              ),
    path('admin/shop/edit',             shop.edit              ),
    path('admin/shop/form',             shop.form              ),
    path('admin/shop/type',             shop.type              ),
    path('admin/shop/delete',           shop.delete            ),

    path('admin/user/list',             user.list              ),
    path('admin/user/edit',             user.edit              ),
    path('admin/user/form',             user.form              ),
    path('admin/user/delete',           user.delete            ),

    path('admin/label/add',             label.add              ),
    path('admin/label/list',            label.list             ),
    path('admin/label/edit',            label.edit             ),
    path('admin/label/view',            label.view             ),
    path('admin/label/form',            label.form             ),
    path('admin/label/delete',          label.delete           ),
    path('admin/label/get',             label.get              ),

    path('admin/order/list',            order.list             ),
    path('admin/order/change_status',   order.change_status    ),
    path('admin/order/view',            order.view             ),


    path('admin/query/list',            query.list             ),
    path('admin/query/view',            query.view             ),
    path('admin/query/replay',          query.replay           ),
    path('admin/query/change_status',   query.change_status    ),
]
