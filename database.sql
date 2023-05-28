
CREATE TABLE CLIENTE(

    id_cliente NUMBER(10) NOT NULL,
    nombre VARCHAR2(20 CHAR) NULL,
    apellido VARCHAR2(20 CHAR) NULL,
    username VARCHAR2(60 CHAR) NOT NULL,
    correo VARCHAR2(255 CHAR) NOT NULL,
    contrasenia VARCHAR2(8 CHAR) NOT NULL,
    
    CONSTRAINT pk_id_cliente PRIMARY KEY (id_cliente)
);

CREATE TABLE PROVEEDOR(

    id_proveedor NUMBER(10) NOT NULL,
    nombre VARCHAR2(20 CHAR) NOT NULL,
    apellido VARCHAR2(20 CHAR) NOT NULL,
    correo VARCHAR2(255 CHAR) NOT NULL,
    telefono NUMBER(9) NOT NULL,
    
    CONSTRAINT pk_id_proveedor PRIMARY KEY (id_proveedor)
);

CREATE TABLE CARRITO(
    
    id_carrito NUMBER(10) NOT NULL,
    creado DATE DEFAULT SYSDATE NOT NULL,
    precio_total NUMBER(10) NOT NULL,
    cantidad_total NUMBER(10) NOT NULL,
    productos_total NUMBER(10) NOT NULL,
    id_cliente NUMBER(10) NOT NULL,
    
    CONSTRAINT pk_id_carrito PRIMARY KEY (id_carrito),
    CONSTRAINT fk_carrito_cliente FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id_cliente)
);

CREATE TABLE COMPRA(

    id_compra NUMBER(10) NOT NULL,
    code VARCHAR2(32 CHAR) NOT NULL,
    fecha_emision DATE DEFAULT SYSDATE NOT NULL,
    precio_total NUMBER(10) NOT NULL,
    productos VARCHAR2(255 CHAR) NOT NULl,
    cantidad_productos NUMBER(10) NOT NULL,
    estado CHAR(1) DEFAULT '1' NOT NULL,
    id_carrito NUMBER(10) NOT NULL,
    
    CONSTRAINT pk_id_compra PRIMARY KEY (id_compra),
    CONSTRAINT fk_compra_carrito FOREIGN KEY (id_carrito) REFERENCES CARRITO(id_carrito)
);

CREATE TABLE BODEGA(
    
    id_bodega NUMBER(10) NOT NULL,
    nombre VARCHAR2(40 CHAR) UNIQUE NOT NULL,
    direccion VARCHAR2(255 CHAR) NOT NULL,
    temperatura NUMBER(3) NOT NULL,
    capacidad NUMBER(10) NOT NULL,
    capacidad_ocupada NUMBER(10) DEFAULT 0 NOT NULL,
    
    CONSTRAINT pk_id_bodega PRIMARY KEY (id_bodega)
);

CREATE TABLE CARGO(

    id_cargo NUMBER(10) NOT NULL,
    nombre VARCHAR2(40 CHAR) NOT NULL,

    CONSTRAINT pk_id_cargo PRIMARY KEY (id_cargo)
);

CREATE TABLE OFERTA(

    id_oferta NUMBER(10) NOT NULL,
    nombre VARCHAR2(40 CHAR) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_termino DATE NOT NULL,
    estado CHAR(1) NOT NULL,
    descuento NUMBER(3) NOT NULL,

    CONSTRAINT pk_id_oferta PRIMARY KEY (id_oferta)
);

CREATE TABLE CATEGORIA(

    id_categoria NUMBER(10) NOT NULL,
    nombre VARCHAR2(40 CHAR) NOT NULL,

    CONSTRAINT pk_id_categoria PRIMARY KEY (id_categoria)
);

CREATE TABLE PRODUCTO(

    id_producto NUMBER(10) NOT NULL,
    nombre VARCHAR2(100 CHAR) NOT NULL,
    precio NUMBER(10) NOT NULL,
    stock NUMBER(10) DEFAULT 0 NOT NULL,
    disponible CHAR(1) DEFAULT '0' NOT NULL,
    creado DATE DEFAULT SYSDATE NOT NULL,
    descripcion VARCHAR2(255 CHAR) NULL,
    id_categoria NUMBER(10) NOT NULL,
    id_oferta NUMBER(10) NULL,
    
    CONSTRAINT pk_id_producto PRIMARY KEY (id_producto),
    CONSTRAINT fk_producto_categoria FOREIGN KEY (id_categoria) REFERENCES CATEGORIA(id_categoria),
    CONSTRAINT fk_producto_oferta FOREIGN KEY (id_oferta) REFERENCES OFERTA(id_oferta)
);

CREATE TABLE ITEMS(
    
    id_items NUMBER(10) NOT NULL,
    cantidad NUMBER(10) NOT NULL,
    id_producto NUMBER(10) NOT NULL,
    id_carrito NUMBER(10) NOT NULL,
    
    CONSTRAINT pk_id_items PRIMARY KEY (id_items),
    CONSTRAINT fk_items_producto FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id_producto),
    CONSTRAINT fk_items_carrito FOREIGN KEY (id_carrito) REFERENCES CARRITO(id_carrito)
);

CREATE TABLE DETALLE_BODEGA(
    
    id_detalle_bodega NUMBER(10) NOT NULL,
    cantidad NUMBER(10) NOT NULL,
    id_bodega NUMBER(10) NOT NULL,
    id_producto NUMBER(10) NOT NULL,
    
    CONSTRAINT pk_id_detalle_bodega PRIMARY KEY (id_detalle_bodega),
    CONSTRAINT fk_detalle_sucursal_bodega FOREIGN KEY (id_bodega) REFERENCES BODEGA(id_bodega),
    CONSTRAINT fk_detalle_sucursal_producto FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id_producto)
);

CREATE TABLE REGION(

    id_region NUMBER(10) NOT NULL,
    nombre VARCHAR2(40 CHAR) NOT NULL,
    sigla VARCHAR2(6 CHAR) NULL,

    CONSTRAINT pk_id_region PRIMARY KEY (id_region)
);

CREATE TABLE PROVINCIA(

    id_provincia NUMBER(10) NOT NULL,
    nombre VARCHAR2(40 CHAR) NOT NULL,
    id_region NUMBER(10) NOT NULL,

    CONSTRAINT pk_id_provincia PRIMARY KEY (id_provincia),
    CONSTRAINT fk_region_provincia FOREIGN KEY (id_region) REFERENCES REGION(id_region)
);

CREATE TABLE COMUNA(

    id_comuna NUMBER(10) NOT NULL,
    nombre VARCHAR2(40 CHAR) NOT NULL,
    id_provincia NUMBER(10) NOT NULL,

    CONSTRAINT pk_id_comuna PRIMARY KEY (id_comuna),
    CONSTRAINT fk_provincia_comuna FOREIGN KEY (id_provincia) REFERENCES PROVINCIA(id_provincia)
);

CREATE TABLE SUCURSAL(
    
    id_sucursal NUMBER(10) NOT NULL,
    nombre VARCHAR2(100 CHAR) NOT NULL,
    razon_social VARCHAR2(60 CHAR) NOT NULL,
    direccion VARCHAR2(255 CHAR) NOT NULL,
    id_comuna NUMBER(10) NOT NULL,
    
    CONSTRAINT pk_id_sucursal PRIMARY KEY (id_sucursal),
    CONSTRAINT fk_comuna_sucursal FOREIGN KEY (id_comuna) REFERENCES COMUNA(id_comuna)
);

CREATE TABLE EMPLEADO(
    
    id_empleado NUMBER(10) NOT NULL,
    nombre VARCHAR2(20 CHAR) NOT NULL,
    apellido VARCHAR2(20 CHAR) NOT NULL,
    run NUMBER(8) NOT NULL,
    dv VARCHAR2(1 CHAR) NOT NULL,
    correo VARCHAR2(255 CHAR) NOT NULL,
    fecha_contrato DATE DEFAULT SYSDATE NOT NULL,
    salario NUMBER(10) NOT NULL,
    id_cargo NUMBER(10) NOT NULL,
    id_sucursal NUMBER(10) NOT NULL,
    
    CONSTRAINT pk_id_sucursal PRIMARY KEY (id_sucursal),
    CONSTRAINT fk_empleado_sucursal FOREIGN KEY (id_sucursal) REFERENCES SUCURSAL(id_sucursal),
    CONSTRAINT fk_empleado_cargo FOREIGN KEY (id_cargo) REFERENCES CARGO(id_cargo)
);

CREATE TABLE DETALLE_SUCURSAL(
    
    id_detalle_sucursal NUMBER(10) NOT NULL,
    cantidad NUMBER(10) NOT NULL,
    id_sucursal NUMBER(10) NOT NULL,
    id_producto NUMBER(10) NOT NULL,
    
    CONSTRAINT pk_id_detalle_sucursal PRIMARY KEY (id_detalle_sucursal),
    CONSTRAINT fk_detalle_sucursal_sucursal FOREIGN KEY (id_sucursal) REFERENCES SUCURSAL(id_sucursal),
    CONSTRAINT fk_detalle_sucursal_producto FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id_producto)
);

CREATE TABLE PEDIDO_CLIENTE(
    
    id_pedido_cliente NUMBER(10) NOT NULL,
    code VARCHAR2(32 CHAR) UNIQUE NOT NULL,
    creado DATE DEFAULT SYSDATE NOT NULL,
    tipo_retiro VARCHAR2(20 CHAR) NOT NULL,
    condicion VARCHAR2(20 CHAR) NOT NULL,
    direccion VARCHAR2(255 CHAR) NULL,
    id_sucursal NUMBER(10) NULL,
    id_comuna NUMBER(10) NULL,
    id_compra NUMBER(10) NOT NULL,
    
    CONSTRAINT pk_id_pedido_cliente PRIMARY KEY (id_pedido_cliente),
    CONSTRAINT fk_pedido_cliente_sucursal FOREIGN KEY (id_sucursal) REFERENCES SUCURSAL(id_sucursal),
    CONSTRAINT fk_pedido_cliente_comuna FOREIGN KEY (id_comuna) REFERENCES COMUNA(id_comuna),
    CONSTRAINT fk_pedido_cliente_compra FOREIGN KEY (id_compra) REFERENCES COMPRA(id_compra)
);

CREATE TABLE BODEGUERO(

    id_bodeguero NUMBER(10) NOT NULL,
    nombre VARCHAR2(20 CHAR) NULL,
    apellido VARCHAR2(20 CHAR) NULL,
    correo VARCHAR2(255 CHAR) UNIQUE NOT NULL,
    telefono NUMBER(9) NOT NULL,
    id_bodega NUMBER(10) NOT NULl,
    
    CONSTRAINT pk_id_bodeguero PRIMARY KEY (id_pedido_cliente),
    CONSTRAINT fk_bodeguero_bodega FOREIGN KEY (id_bodega) REFERENCES BODEGA(id_bodega)
);

CREATE TABLE GUIA_DESPACHO(
    
    id_guia_despacho NUMBER(10) NOT NULL,
    disponible CHAR(1) DEFAULT '1' NOT NULL,
    fecha_emision DATE DEFAULT SYSDATE NOT NULL,
    estado VARCHAR2(40 CHAR) NOT NULL,
    destino VARCHAR2(255 CHAR) NOT NULL,
    id_sucursal NUMBER(10) NOT NULL,
    id_bodeguero NUMBER(10) NOT NULL,
    
    CONSTRAINT pk_id_guia_despacho PRIMARY KEY (id_guia_despacho),
    CONSTRAINT fk_guia_despacho_sucursal FOREIGN KEY (id_sucursal) REFERENCES SUCURSAL(id_sucursal),
    CONSTRAINT fk_guia_despacho_bodeguero FOREIGN KEY (id_bodeguero) REFERENCES BODEGUERO(id_bodeguero)
);

CREATE TABLE PEDIDO(

    id_pedido NUMBER(10) NOT NULL,
    fecha_emision DATE DEFAULT SYSDATE NOT NULL,
    estado VARCHAR2(40 CHAR) NOT NULL,
    destino VARCHAR2(255 CHAR) NOT NULL,
    id_bodeguero NUMBER(10) NOT NULL,
    id_proveedor NUMBER(10) NOT NULL,
    
    CONSTRAINT pk_id_pedido PRIMARY KEY (id_pedido),
    CONSTRAINT fk_pedido_bodeguero FOREIGN KEY (id_bodeguero) REFERENCES BODEGUERO(id_bodeguero),
    CONSTRAINT fk_pedido_proveedor FOREIGN KEY (id_proveedor) REFERENCES PROVEEDOR(id_proveedor)
);

CREATE TABLE PRODUCTO_PEDIDO(

    id_producto_pedido NUMBER(10) NOT NULL,
    cantidad NUMBER(10) NOT NULL,
    id_pedido NUMBER(10) NOT NULL,
    id_producto NUMBER(10) NOT NULL,
    
    CONSTRAINT pk_id_producto_pedido PRIMARY KEY (id_producto_pedido),
    CONSTRAINT fk_producto_pedido_pedido FOREIGN KEY (id_pedido) REFERENCES PEDIDO(id_pedido),
    CONSTRAINT fk_producto_pedido_producto FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id_producto)
);
