
DROP TABLE DETALLE_BODEGA;
DROP TABLE DETALLE_SUCURSAL;
DROP TABLE PRODUCTO_DESPACHO;
DROP TABLE ORDEN_PEDIDO;
DROP TABLE PEDIDO_CLIENTE;
DROP TABLE ORDEN;
DROP TABLE PEDIDO;
DROP TABLE FACTURA;
DROP TABLE PROVEEDOR;
DROP TABLE GUIA_DESPACHO;
DROP TABLE BODEGUERO;
DROP TABLE BODEGA;
DROP TABLE COMPRA;
DROP TABLE ITEMS;
DROP TABLE CARRITO;
DROP TABLE CLIENTE;
DROP TABLE USUARIO;
DROP TABLE EMPLEADO;
DROP TABLE CARGO;
DROP TABLE SUCURSAL;
DROP TABLE COMUNA;
DROP TABLE PROVINCIA;
DROP TABLE REGION;
DROP TABLE PRODUCTO;
DROP TABLE CATEGORIA;
DROP TABLE OFERTA;

DROP SEQUENCE id_auto_incremental;

CREATE SEQUENCE id_auto_incremental
  START WITH 1
  INCREMENT BY 1
  NOMAXVALUE
  NOCYCLE;

CREATE TABLE USUARIO(

    id_usuario INTEGER NOT NULL,
    nombre VARCHAR2(20 CHAR) NULL,
    apellido VARCHAR2(20 CHAR) NULL,
    username VARCHAR2(60 CHAR) UNIQUE NOT NULL,
    correo VARCHAR2(255 CHAR) UNIQUE NOT NULL,
    contrasenia VARCHAR2(8 CHAR) UNIQUE NOT NULL,
    
    CONSTRAINT pk_id_usuario PRIMARY KEY (id_usuario)
);

ALTER TABLE USUARIO MODIFY id_usuario INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE CLIENTE(

    id_cliente INTEGER NOT NULL,
    nombre VARCHAR2(20 CHAR) NULL,
    apellido VARCHAR2(20 CHAR) NULL,
    run NUMBER(8) UNIQUE NOT NULL,
    dv VARCHAR2(1 CHAR) NOT NULL,
    correo VARCHAR2(255 CHAR) UNIQUE NOT NULL,
    telefono VARCHAR2(12 CHAR) UNIQUE NOT NULL,
    id_usuario INTEGER NOT NULL,
    
    CONSTRAINT pk_id_cliente PRIMARY KEY (id_cliente),
    CONSTRAINT fk_cliente_usuario FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario)
);

ALTER TABLE CLIENTE MODIFY id_cliente INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE PROVEEDOR(

    id_proveedor INTEGER NOT NULL,
    nombre VARCHAR2(20 CHAR) NOT NULL,
    apellido VARCHAR2(20 CHAR) NOT NULL,
    correo VARCHAR2(255 CHAR) UNIQUE NOT NULL,
    telefono NUMBER(9) NOT NULL,
    
    CONSTRAINT pk_id_proveedor PRIMARY KEY (id_proveedor)
);

ALTER TABLE PROVEEDOR MODIFY id_proveedor INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE CARRITO(
    
    id_carrito INTEGER NOT NULL,
    creado DATE DEFAULT SYSDATE NOT NULL,
    precio_total NUMBER(10) NOT NULL,
    cantidad_total NUMBER(10) NOT NULL,
    productos_total NUMBER(10) NOT NULL,
    id_cliente INTEGER NOT NULL,
    
    CONSTRAINT pk_id_carrito PRIMARY KEY (id_carrito),
    CONSTRAINT fk_carrito_cliente FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id_cliente)
);

ALTER TABLE CARRITO MODIFY id_carrito INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE COMPRA(

    id_compra INTEGER NOT NULL,
    code VARCHAR2(32 CHAR) UNIQUE NOT NULL,
    fecha_emision DATE DEFAULT SYSDATE NOT NULL,
    precio_total NUMBER(10) NOT NULL,
    productos CLOB NOT NULl,
    cantidad_productos NUMBER(10) NOT NULL,
    estado CHAR(1) DEFAULT '1' NOT NULL,
    id_carrito INTEGER NOT NULL,
    
    CONSTRAINT pk_id_compra PRIMARY KEY (id_compra),
    CONSTRAINT fk_compra_carrito FOREIGN KEY (id_carrito) REFERENCES CARRITO(id_carrito)
);

ALTER TABLE COMPRA MODIFY id_compra INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE BODEGA(
    
    id_bodega INTEGER NOT NULL,
    nombre VARCHAR2(40 CHAR) UNIQUE NOT NULL,
    direccion VARCHAR2(255 CHAR) NOT NULL,
    temperatura NUMBER(3) NOT NULL,
    capacidad NUMBER(10) NOT NULL,
    capacidad_ocupada NUMBER(10) DEFAULT 0 NOT NULL,
    
    CONSTRAINT pk_id_bodega PRIMARY KEY (id_bodega)
);

ALTER TABLE bodega MODIFY id_bodega INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE CARGO(

    id_cargo INTEGER NOT NULL,
    nombre VARCHAR2(40 CHAR) UNIQUE NOT NULL,

    CONSTRAINT pk_id_cargo PRIMARY KEY (id_cargo)
);

ALTER TABLE CARGO MODIFY id_cargo INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE OFERTA(

    id_oferta INTEGER NOT NULL,
    nombre VARCHAR2(40 CHAR) NOT NULL,
    fecha_inicio DATE DEFAULT SYSDATE NOT NULL,
    fecha_termino DATE NOT NULL,
    estado CHAR(1) DEFAULT '1' NOT NULL,
    descuento NUMBER(3) NOT NULL,

    CONSTRAINT pk_id_oferta PRIMARY KEY (id_oferta)
);

ALTER TABLE OFERTA MODIFY id_oferta INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE CATEGORIA(

    id_categoria INTEGER NOT NULL,
    nombre VARCHAR2(40 CHAR) NOT NULL,

    CONSTRAINT pk_id_categoria PRIMARY KEY (id_categoria)
);

ALTER TABLE CATEGORIA MODIFY id_categoria INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE PRODUCTO(

    id_producto INTEGER NOT NULL,
    nombre VARCHAR2(100 CHAR) UNIQUE NOT NULL,
    precio NUMBER(10) NOT NULL,
    stock NUMBER(10) DEFAULT 0 NOT NULL,
    disponible CHAR(1) DEFAULT '0' NOT NULL,
    creado DATE DEFAULT SYSDATE NOT NULL,
    descripcion VARCHAR2(255 CHAR) NULL,
    id_categoria INTEGER NOT NULL,
    id_oferta INTEGER NULL,
    
    CONSTRAINT pk_id_producto PRIMARY KEY (id_producto),
    CONSTRAINT fk_producto_categoria FOREIGN KEY (id_categoria) REFERENCES CATEGORIA(id_categoria),
    CONSTRAINT fk_producto_oferta FOREIGN KEY (id_oferta) REFERENCES OFERTA(id_oferta)
);

ALTER TABLE PRODUCTO MODIFY id_producto INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE ITEMS(
    
    id_items INTEGER NOT NULL,
    cantidad NUMBER(10) NOT NULL,
    id_producto INTEGER NOT NULL,
    id_carrito INTEGER NOT NULL,
    
    CONSTRAINT pk_id_items PRIMARY KEY (id_items),
    CONSTRAINT fk_items_producto FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id_producto),
    CONSTRAINT fk_items_carrito FOREIGN KEY (id_carrito) REFERENCES CARRITO(id_carrito)
);

ALTER TABLE ITEMS MODIFY id_items INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE DETALLE_BODEGA(
    
    id_detalle_bodega INTEGER NOT NULL,
    cantidad NUMBER(10) NOT NULL,
    id_bodega INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    
    CONSTRAINT pk_id_detalle_bodega PRIMARY KEY (id_detalle_bodega),
    CONSTRAINT fk_detalle_bodega_bodega FOREIGN KEY (id_bodega) REFERENCES BODEGA(id_bodega),
    CONSTRAINT fk_detalle_bodega_producto FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id_producto)
);

ALTER TABLE DETALLE_BODEGA MODIFY id_detalle_bodega INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE REGION(

    id_region INTEGER NOT NULL,
    nombre VARCHAR2(100 CHAR) UNIQUE NOT NULL,
    sigla VARCHAR2(6 CHAR) NULL,

    CONSTRAINT pk_id_region PRIMARY KEY (id_region)
);

ALTER TABLE REGION MODIFY id_region INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE PROVINCIA(

    id_provincia INTEGER NOT NULL,
    nombre VARCHAR2(100 CHAR) UNIQUE NOT NULL,
    id_region INTEGER NOT NULL,

    CONSTRAINT pk_id_provincia PRIMARY KEY (id_provincia),
    CONSTRAINT fk_region_provincia FOREIGN KEY (id_region) REFERENCES REGION(id_region)
);

ALTER TABLE PROVINCIA MODIFY id_provincia INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE COMUNA(

    id_comuna INTEGER NOT NULL,
    nombre VARCHAR2(40 CHAR) UNIQUE NOT NULL,
    id_provincia INTEGER NOT NULL,

    CONSTRAINT pk_id_comuna PRIMARY KEY (id_comuna),
    CONSTRAINT fk_provincia_comuna FOREIGN KEY (id_provincia) REFERENCES PROVINCIA(id_provincia)
);

ALTER TABLE COMUNA MODIFY id_comuna INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE SUCURSAL(
    
    id_sucursal INTEGER NOT NULL,
    nombre VARCHAR2(100 CHAR) UNIQUE NOT NULL,
    razon_social VARCHAR2(60 CHAR) UNIQUE NOT NULL,
    direccion VARCHAR2(255 CHAR) NOT NULL,
    id_comuna INTEGER NOT NULL,
    
    CONSTRAINT pk_id_sucursal PRIMARY KEY (id_sucursal),
    CONSTRAINT fk_comuna_sucursal FOREIGN KEY (id_comuna) REFERENCES COMUNA(id_comuna)
);

ALTER TABLE SUCURSAL MODIFY id_sucursal INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE EMPLEADO(
    
    id_empleado INTEGER NOT NULL,
    nombre VARCHAR2(20 CHAR) NOT NULL,
    apellido VARCHAR2(20 CHAR) NOT NULL,
    run NUMBER(8) UNIQUE NOT NULL,
    dv VARCHAR2(1 CHAR) NOT NULL,
    correo VARCHAR2(255 CHAR) UNIQUE NOT NULL,
    fecha_contrato DATE DEFAULT SYSDATE NOT NULL,
    salario NUMBER(10) NOT NULL,
    id_cargo INTEGER NOT NULL,
    id_sucursal INTEGER NOT NULL,
    
    CONSTRAINT pk_id_empleado PRIMARY KEY (id_empleado),
    CONSTRAINT fk_empleado_sucursal FOREIGN KEY (id_sucursal) REFERENCES SUCURSAL(id_sucursal),
    CONSTRAINT fk_empleado_cargo FOREIGN KEY (id_cargo) REFERENCES CARGO(id_cargo)
);

ALTER TABLE EMPLEADO MODIFY id_empleado INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE DETALLE_SUCURSAL(
    
    id_detalle_sucursal INTEGER NOT NULL,
    cantidad NUMBER(10) NOT NULL,
    id_sucursal INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    
    CONSTRAINT pk_id_detalle_sucursal PRIMARY KEY (id_detalle_sucursal),
    CONSTRAINT fk_detalle_sucursal_sucursal FOREIGN KEY (id_sucursal) REFERENCES SUCURSAL(id_sucursal),
    CONSTRAINT fk_detalle_sucursal_producto FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id_producto)
);

ALTER TABLE DETALLE_SUCURSAL MODIFY id_detalle_sucursal INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE PEDIDO_CLIENTE(
    
    id_pedido_cliente INTEGER NOT NULL,
    code VARCHAR2(32 CHAR) UNIQUE NOT NULL,
    creado DATE DEFAULT SYSDATE NOT NULL,
    tipo_retiro VARCHAR2(20 CHAR) NOT NULL,
    condicion VARCHAR2(20 CHAR) DEFAULT 'en preparacion' NOT NULL,
    direccion VARCHAR2(255 CHAR) NULL,
    id_sucursal INTEGER NULL,
    id_comuna INTEGER NULL,
    id_compra INTEGER NOT NULL,
    
    CONSTRAINT pk_id_pedido_cliente PRIMARY KEY (id_pedido_cliente),
    CONSTRAINT fk_pedido_cliente_sucursal FOREIGN KEY (id_sucursal) REFERENCES SUCURSAL(id_sucursal),
    CONSTRAINT fk_pedido_cliente_comuna FOREIGN KEY (id_comuna) REFERENCES COMUNA(id_comuna),
    CONSTRAINT fk_pedido_cliente_compra FOREIGN KEY (id_compra) REFERENCES COMPRA(id_compra)
);

ALTER TABLE PEDIDO_CLIENTE MODIFY id_pedido_cliente INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE BODEGUERO(

    id_bodeguero INTEGER NOT NULL,
    nombre VARCHAR2(20 CHAR) NULL,
    apellido VARCHAR2(20 CHAR) NULL,
    correo VARCHAR2(255 CHAR) UNIQUE NOT NULL,
    telefono NUMBER(9) NOT NULL,
    id_bodega INTEGER NOT NULl,
    
    CONSTRAINT pk_id_bodeguero PRIMARY KEY (id_bodeguero),
    CONSTRAINT fk_bodeguero_bodega FOREIGN KEY (id_bodega) REFERENCES BODEGA(id_bodega)
);

ALTER TABLE BODEGUERO MODIFY id_bodeguero INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE GUIA_DESPACHO(
    
    id_guia_despacho INTEGER NOT NULL,
    disponible CHAR(1) DEFAULT '1' NOT NULL,
    fecha_emision DATE DEFAULT SYSDATE NOT NULL,
    estado VARCHAR2(40 CHAR) NOT NULL,
    destino VARCHAR2(255 CHAR) NOT NULL,
    id_sucursal INTEGER NOT NULL,
    id_bodeguero INTEGER NOT NULL,
    
    CONSTRAINT pk_id_guia_despacho PRIMARY KEY (id_guia_despacho),
    CONSTRAINT fk_guia_despacho_sucursal FOREIGN KEY (id_sucursal) REFERENCES SUCURSAL(id_sucursal),
    CONSTRAINT fk_guia_despacho_bodeguero FOREIGN KEY (id_bodeguero) REFERENCES BODEGUERO(id_bodeguero)
);

ALTER TABLE GUIA_DESPACHO MODIFY id_guia_despacho INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE PRODUCTO_DESPACHO(
    
    id_producto_despacho INTEGER NOT NULL,
    cantidad NUMBER(10) NOT NULL,
    id_guia_despacho INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    
    CONSTRAINT pk_id_producto_despacho PRIMARY KEY (id_producto_despacho),
    CONSTRAINT fk_producto_despacho_guia_despacho FOREIGN KEY (id_guia_despacho) REFERENCES GUIA_DESPACHO(id_guia_despacho),
    CONSTRAINT fk_producto_despacho_producto FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id_producto)
);

ALTER TABLE PRODUCTO_DESPACHO MODIFY id_producto_despacho INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE FACTURA(

    id_factura INTEGER NOT NULL,
    code VARCHAR2(32 CHAR) NOT NULL,
    fecha_emicion DATE NOT NULL,
    productos CLOB NOT NULL,
    precio_total NUMBER(10) NOT NULL,
    cantidad_total NUMBER(10) NOT NULL,
    id_bodeguero INTEGER NOT NULL,
    id_proveedor INTEGER NOT NULL,
    
    CONSTRAINT pk_id_factura PRIMARY KEY(id_factura),
    CONSTRAINT fk_factura_bodeguero FOREIGN KEY (id_bodeguero) REFERENCES BODEGUERO(id_bodeguero),
    CONSTRAINT fk_factura_proveedor FOREIGN KEY (id_proveedor) REFERENCES PROVEEDOR(id_proveedor)
);

ALTER TABLE FACTURA MODIFY id_factura INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE PEDIDO(
    id_pedido INTEGER NOT NULL,
    fecha_emision DATE DEFAULT SYSDATE NOT NULL,
    estado VARCHAR2(40 CHAR) NOT NULL,
    destino VARCHAR2(255 CHAR) NOT NULL,
    id_bodeguero INTEGER NOT NULL,
    id_factura INTEGER NOT NULL,
    
    CONSTRAINT pk_id_pedido PRIMARY KEY (id_pedido),
    CONSTRAINT fk_pedido_bodeguero FOREIGN KEY (id_bodeguero) REFERENCES BODEGUERO(id_bodeguero),
    CONSTRAINT fk_pedido_factura FOREIGN KEY (id_factura) REFERENCES FACTURA(id_factura)
);

ALTER TABLE PEDIDO MODIFY id_pedido INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE ORDEN(

    id_orden INTEGER NOT NULL,
    fecha_emicion DATE DEFAULT SYSDATE NOT NULL,
    estado VARCHAR2(40 CHAR) NOT NULL,
    id_empleado INTEGER NOT NULL,
    id_bodeguero INTEGER NOT NULL,
    
    CONSTRAINT pk_id_orden PRIMARY KEY (id_orden),
    CONSTRAINT fk_orden_empleado FOREIGN KEY (id_empleado) REFERENCES EMPLEADO(id_empleado),
    CONSTRAINT fk_orden_bodeguero FOREIGN KEY (id_bodeguero) REFERENCES BODEGUERO(id_bodeguero)
);

ALTER TABLE ORDEN MODIFY id_orden INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

CREATE TABLE ORDEN_PEDIDO(

    id_orden_pedido INTEGER NOT NULL,
    cantidad NUMBER(10) NOT NULL,
    id_orden INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    
    CONSTRAINT pk_id_orden_pedido PRIMARY KEY (id_orden_pedido),
    CONSTRAINT fk_orden_pedido_orden FOREIGN KEY (id_orden) REFERENCES ORDEN(id_orden),
    CONSTRAINT fk_orden_pedido_producto FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id_producto)
);

ALTER TABLE ORDEN_PEDIDO MODIFY id_orden_pedido INTEGER DEFAULT ID_AUTO_INCREMENTAL.NEXTVAL;

INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(1, 'bodega nunoa', 'calle agustin correa bravo', 25, 200000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(2, 'bodega curico', 'calle alberto baines 6354', 23, 600000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(3, 'bodega santiago', 'calle alfonso paulino 4732', 23, 800000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(4, 'bodega maipu', 'calle arauco 3243', 20, 1000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(5, 'bodega el bosque', 'calle av. gonzales 9324', 19, 2000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(6, 'bodega san bernardo', 'calle colon 3647', 18, 4000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(7, 'bodega araucania', 'calle barros torres 3026', 15, 6000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(8, 'bodega concepcion', 'calle vickuna mackena 7348', 18, 4000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(9, 'bodega los angeles', 'calle carlos wilson 8432', 22, 5000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(10, 'bodega punta arenas', 'calle cinco de abril 1683', 24, 9000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(11, 'bodega rancuagua', 'calle concepcion 9327', 20, 300000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(12, 'bodega arica', 'calle concordia 8734', 23, 400000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(13, 'bodega coquimbo', 'calle conde del maule 8433', 21, 800000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(14, 'bodega san fernando', 'calle coronel del canto 9127', 20, 1000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(15, 'bodega chillan', 'calle av. maza 7329', 26, 5000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(16, 'bodega los rios', 'calle causino prieto 7382', 14, 9000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(17, 'bodega los lagos', 'calle cristobal escobar 7483', 15, 3000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(18, 'bodega independencia', 'calle av. chacabuco 4378', 20, 6000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(19, 'bodega la reina', 'calle av. de la cruz 4783', 20, 8000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(20, 'bodega puente alto', 'calle siete de abril 9348', 24, 8000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(21, 'bodega valparaiso', 'calle av. balmaceda 4378', 21, 600000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(22, 'bodega la serena', 'calle barros luco 9347', 26, 1000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(23, 'bodega antofagasta', 'calle carlos walker 8032', 21, 800000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(24, 'bodega san esteban', 'calle comandante canales 3948', 19, 1000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(25, 'bodega buin', 'calle constitucion 9348', 20, 7000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(26, 'bodega paine', 'calle av. correa 8347', 18, 9000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(27, 'bodega linderos', 'calle doctor garzia 6478', 13, 4000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(28, 'bodega lo espejo', 'calle eduardo matte 3264', 28, 9000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(29, 'bodega pichilemu', 'calle emiliano figueroa 1845', 21, 1000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(30, 'bodega concon', 'calle estados unidos 7483', 24, 2000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(31, 'bodega la florida', 'calle federico froebel 7345', 18, 800000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(32, 'bodega macul', 'calle francisco lobos 6342', 23, 2000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(33, 'bodega vicuna', 'calle garcia valenzuela 5489', 25, 900000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(34, 'bodega los andes', 'calle general miranda 3478', 20, 200000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(35, 'bodega calama', 'calle granaderos 8327', 21, 8000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(36, 'bodega chiloe', 'calle av. gutenberg 4326', 20, 4000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(37, 'bodega talca', 'calle huasco 9324', 16, 8000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(38, 'bodega llanquihue', 'calle hurtado de mendoza 4332', 24, 6000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(39, 'bodega recoleta', 'calle joaquin martinez 5473', 22, 400000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(40, 'bodega renca', 'calle irene morales 7863', 16, 1000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(41, 'bodega la ligua', 'calle jose alfonso 3421', 16, 700000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(42, 'bodega quintero', 'calle jose arrieta 6534', 19, 5000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(43, 'bodega general lagos', 'calle jose miguel calvo 5432', 21, 400000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(44, 'bodega providencia', 'calle jose victorino lastarria 3456', 28, 300000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(45, 'bodega estacion central', 'calle juan godoy 5346', 27, 8000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(46, 'bodega los vilos', 'calle julia teresa 7683', 21, 9000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(47, 'bodega magallanes', 'calle la colonia 5432', 23, 6000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(48, 'bodega ovalle', 'calle la estrella 5342', 24, 7000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(49, 'bodega tocopilla', 'calle la montana 5343', 14, 1000000);
INSERT INTO BODEGA (id_bodega, nombre, direccion, temperatura, capacidad) VALUES(50, 'bodega pedro aguirrez cerda', 'calle la plata 6452', 16, 1000000);

INSERT INTO REGION VALUES(1, 'Arica y Parinacota', 'XV');
INSERT INTO REGION VALUES(2, 'Tarapaca', 'I');
INSERT INTO REGION VALUES(3, 'Antofagasta', 'II');
INSERT INTO REGION VALUES(4, 'Atacama', 'III');
INSERT INTO REGION VALUES(5, 'Coquimbo', 'IV');
INSERT INTO REGION VALUES(6, 'Valparaiso', 'V');
INSERT INTO REGION VALUES(7, 'Libertador General Bernardo OHiggins', 'VI');
INSERT INTO REGION VALUES(8, 'Maule', 'VII');
INSERT INTO REGION VALUES(9, 'Nuble', 'XVI');
INSERT INTO REGION VALUES(10, 'Biobio', 'VIII');
INSERT INTO REGION VALUES(11, 'La Araucania', 'IX');
INSERT INTO REGION VALUES(12, 'Los Rios', 'XIV');
INSERT INTO REGION VALUES(13, 'Los Lagos', 'X');
INSERT INTO REGION VALUES(14, 'Aysen del General Carlos Ibanez del Campo', 'XI');
INSERT INTO REGION VALUES(15, 'Magallanes y de la Antartica Chilena ', 'XII');
INSERT INTO REGION VALUES(16, 'Metropolitana de Santiago', '');

INSERT INTO PROVINCIA VALUES(1, 'Arica', 1);
INSERT INTO PROVINCIA VALUES(2, 'Parinacota', 1);

INSERT INTO PROVINCIA VALUES(3, 'Iquique', 2);
INSERT INTO PROVINCIA VALUES(4, 'Tamarugal', 2);

INSERT INTO PROVINCIA VALUES(5, 'Tocopilla', 3);
INSERT INTO PROVINCIA VALUES(6, 'El Loa', 3);
INSERT INTO PROVINCIA VALUES(7, 'Antofagasta', 3);

INSERT INTO PROVINCIA VALUES(8, 'Chanaral', 4);
INSERT INTO PROVINCIA VALUES(9, 'Copiapo', 4);
INSERT INTO PROVINCIA VALUES(10, 'Huasco', 4);

INSERT INTO PROVINCIA VALUES(11, 'Elqui', 5);
INSERT INTO PROVINCIA VALUES(12, 'Limari', 5);
INSERT INTO PROVINCIA VALUES(13, 'Choapa', 5);

INSERT INTO PROVINCIA VALUES(14, 'Petorca', 6);
INSERT INTO PROVINCIA VALUES(15, 'Los Andes', 6);
INSERT INTO PROVINCIA VALUES(16, 'San Felipe de Aconcagua', 6);
INSERT INTO PROVINCIA VALUES(17, 'Quillota', 6);
INSERT INTO PROVINCIA VALUES(18, 'Valparaiso', 6);
INSERT INTO PROVINCIA VALUES(19, 'San Antonio', 6);
INSERT INTO PROVINCIA VALUES(20, 'Isla de Pascua', 6);
INSERT INTO PROVINCIA VALUES(21, 'Marga Marga', 6);

INSERT INTO PROVINCIA VALUES(22, 'Chacabuco', 16);
INSERT INTO PROVINCIA VALUES(23, 'Santiago', 16);
INSERT INTO PROVINCIA VALUES(24, 'Cordillera', 16);
INSERT INTO PROVINCIA VALUES(25, 'Maipo', 16);
INSERT INTO PROVINCIA VALUES(26, 'Melipilla', 16);
INSERT INTO PROVINCIA VALUES(27, 'Talagante', 16);

INSERT INTO PROVINCIA VALUES(28, 'Cachapoal', 7);
INSERT INTO PROVINCIA VALUES(29, 'Colchagua', 7);
INSERT INTO PROVINCIA VALUES(30, ' Cardenal Caro', 7);

INSERT INTO PROVINCIA VALUES(31, 'Curico', 8);
INSERT INTO PROVINCIA VALUES(32, 'Talca', 8);
INSERT INTO PROVINCIA VALUES(33, 'Linares', 8);
INSERT INTO PROVINCIA VALUES(34, 'Cauquenes', 8);

INSERT INTO PROVINCIA VALUES(35, 'Diguillin', 9);
INSERT INTO PROVINCIA VALUES(36, 'Itata', 9);
INSERT INTO PROVINCIA VALUES(37, 'Punilla', 9);

INSERT INTO PROVINCIA VALUES(38, 'Biobio', 10);
INSERT INTO PROVINCIA VALUES(39, 'Concepcion', 10);
INSERT INTO PROVINCIA VALUES(40, 'Arauco', 10);

INSERT INTO PROVINCIA VALUES(41, 'Malleco', 11);
INSERT INTO PROVINCIA VALUES(42, 'Cautin', 11);

INSERT INTO PROVINCIA VALUES(43, 'Valdivia', 12);
INSERT INTO PROVINCIA VALUES(44, 'Ranco', 12);

INSERT INTO PROVINCIA VALUES(45, 'Osorno', 13);
INSERT INTO PROVINCIA VALUES(46, 'Llanquihue', 13);
INSERT INTO PROVINCIA VALUES(47, 'Chiloe', 13);
INSERT INTO PROVINCIA VALUES(48, 'Palena', 13);

INSERT INTO PROVINCIA VALUES(49, 'Coyhaique', 14);
INSERT INTO PROVINCIA VALUES(50, 'Aysen', 14);
INSERT INTO PROVINCIA VALUES(51, 'General Carrera', 14);
INSERT INTO PROVINCIA VALUES(52, 'Capitan Prat', 14);

INSERT INTO PROVINCIA VALUES(53, 'Ultima Esperanza', 15);
INSERT INTO PROVINCIA VALUES(54, 'Magallanes', 15);
INSERT INTO PROVINCIA VALUES(55, 'Tierra del Fuego', 15);
INSERT INTO PROVINCIA VALUES(56, 'Antartica Chilena', 15);

-- Comunas de Chile

INSERT INTO COMUNA VALUES(1, 'Arica', 1);
INSERT INTO COMUNA VALUES(2, 'Camarones', 1);

INSERT INTO COMUNA VALUES(3, 'General Lagos', 2);
INSERT INTO COMUNA VALUES(4, 'Putre', 2);

INSERT INTO COMUNA VALUES(5, 'Alto Hospicio', 3);
INSERT INTO COMUNA VALUES(6, 'Iquique', 3);

INSERT INTO COMUNA VALUES(7, 'Camina', 4);
INSERT INTO COMUNA VALUES(8, 'Colchane', 4);
INSERT INTO COMUNA VALUES(9, 'Huara', 4);
INSERT INTO COMUNA VALUES(10, 'Pica', 4);
INSERT INTO COMUNA VALUES(11, 'Pozo Almonte', 4);

INSERT INTO COMUNA VALUES(12, 'Antofagasta', 7);
INSERT INTO COMUNA VALUES(13, 'Mejillones', 7);
INSERT INTO COMUNA VALUES(14, 'Sierra Gorda', 7);
INSERT INTO COMUNA VALUES(15, 'Taltal', 7);

INSERT INTO COMUNA VALUES(16, 'Calama', 6);
INSERT INTO COMUNA VALUES(17, 'Ollagne', 6);
INSERT INTO COMUNA VALUES(18, 'San Pedro de Atacama', 6);

INSERT INTO COMUNA VALUES(19, 'Maria Elena', 5);
INSERT INTO COMUNA VALUES(20, 'Tocopilla', 5);

INSERT INTO COMUNA VALUES(21, 'Chanaral', 8);
INSERT INTO COMUNA VALUES(22, 'Diego de Almagro', 8);

INSERT INTO COMUNA VALUES(23, 'Caldera', 9);
INSERT INTO COMUNA VALUES(24, 'Copiapo', 9);
INSERT INTO COMUNA VALUES(25, 'Tierra Amarilla', 9);

INSERT INTO COMUNA VALUES(26, 'Alto del Carmen', 10);
INSERT INTO COMUNA VALUES(27, 'Freirina', 10);
INSERT INTO COMUNA VALUES(28, 'Huasco', 10);
INSERT INTO COMUNA VALUES(29, 'Vallenar', 10);

INSERT INTO COMUNA VALUES(30, 'Andacollo', 11);
INSERT INTO COMUNA VALUES(31, 'Coquimbo', 11);
INSERT INTO COMUNA VALUES(32, 'La Higuera', 11);
INSERT INTO COMUNA VALUES(33, 'La Serena', 11);
INSERT INTO COMUNA VALUES(34, 'Paihuano', 11);
INSERT INTO COMUNA VALUES(35, 'Vicuna', 11);

INSERT INTO COMUNA VALUES(36, 'Combarbala', 12);
INSERT INTO COMUNA VALUES(37, 'Monte Patria', 12);
INSERT INTO COMUNA VALUES(38, 'Ovalle', 12);
INSERT INTO COMUNA VALUES(39, 'Punitaqui', 12);
INSERT INTO COMUNA VALUES(40, 'Rio Hurtado', 12);

INSERT INTO COMUNA VALUES(41, 'Canela', 13);
INSERT INTO COMUNA VALUES(42, 'Illapel', 13);
INSERT INTO COMUNA VALUES(43, 'Los Vilos', 13);
INSERT INTO COMUNA VALUES(44, 'Salamanca', 13);

INSERT INTO COMUNA VALUES(45, 'Calle Larga', 15);
INSERT INTO COMUNA VALUES(46, 'Los Andes', 15);
INSERT INTO COMUNA VALUES(47, 'San Esteban', 15);
INSERT INTO COMUNA VALUES(48, 'Rinconada', 15);

INSERT INTO COMUNA VALUES(49, 'Cabildo', 14);
INSERT INTO COMUNA VALUES(50, 'La Ligua', 14);
INSERT INTO COMUNA VALUES(51, 'Papudo', 14);
INSERT INTO COMUNA VALUES(52, 'Petorca', 14);
INSERT INTO COMUNA VALUES(53, 'Zapallar', 14);

INSERT INTO COMUNA VALUES(54, 'Hijuelas', 17);
INSERT INTO COMUNA VALUES(55, 'La Calera', 17);
INSERT INTO COMUNA VALUES(56, 'La Cruz', 17);
INSERT INTO COMUNA VALUES(57, 'Nogales', 17);
INSERT INTO COMUNA VALUES(58, 'Quillota', 17);

INSERT INTO COMUNA VALUES(59, 'Algarrobo', 19);
INSERT INTO COMUNA VALUES(60, 'Cartagena', 19);
INSERT INTO COMUNA VALUES(61, 'El Quisco', 19);
INSERT INTO COMUNA VALUES(62, 'El Tabo', 19);
INSERT INTO COMUNA VALUES(63, 'San Antonio', 19);
INSERT INTO COMUNA VALUES(64, 'Santo Domingo', 19);

INSERT INTO COMUNA VALUES(65, 'Catemu', 16);
INSERT INTO COMUNA VALUES(66, 'Llay-Llay', 16);
INSERT INTO COMUNA VALUES(67, 'Panquehue', 16);
INSERT INTO COMUNA VALUES(68, 'Putaendo', 16);
INSERT INTO COMUNA VALUES(69, 'San Felipe', 16);
INSERT INTO COMUNA VALUES(70, 'Santa Maria', 16);

INSERT INTO COMUNA VALUES(71, 'Vina del Mar', 18);
INSERT INTO COMUNA VALUES(72, 'Valparaiso', 18);
INSERT INTO COMUNA VALUES(73, 'Quintero', 18);
INSERT INTO COMUNA VALUES(74, 'Puchuncavi', 18);
INSERT INTO COMUNA VALUES(75, 'Juan Fernandez', 18);
INSERT INTO COMUNA VALUES(76, 'Concon', 18);
INSERT INTO COMUNA VALUES(77, 'Casablanca', 18);

INSERT INTO COMUNA VALUES(78, 'Villa Alemana', 21);
INSERT INTO COMUNA VALUES(79, 'Quilpue', 21);
INSERT INTO COMUNA VALUES(80, 'Olmue', 21);
INSERT INTO COMUNA VALUES(81, 'Limache', 21);

INSERT INTO COMUNA VALUES(82, 'Rapa Nui', 20);

INSERT INTO COMUNA VALUES(83, 'Colina', 22);
INSERT INTO COMUNA VALUES(84, 'Til Til', 22);
INSERT INTO COMUNA VALUES(85, 'Lampa', 22);

INSERT INTO COMUNA VALUES(86, 'San Jose de Maipo', 24);
INSERT INTO COMUNA VALUES(87, 'Puente Alto', 24);
INSERT INTO COMUNA VALUES(88, 'Pirque', 24);

INSERT INTO COMUNA VALUES(89, 'Calera de Tango', 25);
INSERT INTO COMUNA VALUES(90, 'San Bernardo', 25);
INSERT INTO COMUNA VALUES(91, 'Buin', 25);
INSERT INTO COMUNA VALUES(92, 'Paine', 25);

INSERT INTO COMUNA VALUES(93, 'Alhue', 26);
INSERT INTO COMUNA VALUES(94, 'San Pedro', 26);
INSERT INTO COMUNA VALUES(95, 'Melipilla', 26);
INSERT INTO COMUNA VALUES(96, 'Maria Pinto', 26);
INSERT INTO COMUNA VALUES(97, 'Curacavi', 26);

INSERT INTO COMUNA VALUES(98, 'Cerrillos', 23);
INSERT INTO COMUNA VALUES(99, 'Cerro Navia', 23);
INSERT INTO COMUNA VALUES(100, 'Conchali', 23);
INSERT INTO COMUNA VALUES(101, 'El Bosque', 23);
INSERT INTO COMUNA VALUES(102, 'Estacion Central', 23);
INSERT INTO COMUNA VALUES(103, 'Huechuraba', 23);
INSERT INTO COMUNA VALUES(104, 'Independencia', 23);
INSERT INTO COMUNA VALUES(105, 'La Cisterna', 23);
INSERT INTO COMUNA VALUES(106, 'La Granja', 23);
INSERT INTO COMUNA VALUES(107, 'La Florida', 23);
INSERT INTO COMUNA VALUES(108, 'La Pintana', 23);
INSERT INTO COMUNA VALUES(109, 'La Reina', 23);
INSERT INTO COMUNA VALUES(110, 'Las Condes', 23);
INSERT INTO COMUNA VALUES(111, 'Lo Barnechea', 23);
INSERT INTO COMUNA VALUES(112, 'Lo Espejo', 23);
INSERT INTO COMUNA VALUES(113, 'Lo Prado', 23);
INSERT INTO COMUNA VALUES(114, 'Macul', 23);
INSERT INTO COMUNA VALUES(115, 'Maipu', 23);
INSERT INTO COMUNA VALUES(116, 'nunoa', 23);
INSERT INTO COMUNA VALUES(117, 'Pedro Aguirre Cerda', 23);
INSERT INTO COMUNA VALUES(118, 'Penalolen', 23);
INSERT INTO COMUNA VALUES(119, 'Providencia', 23);
INSERT INTO COMUNA VALUES(120, 'Pudahuel', 23);
INSERT INTO COMUNA VALUES(121, 'Quilicura', 23);
INSERT INTO COMUNA VALUES(122, 'Quinta Normal', 23);
INSERT INTO COMUNA VALUES(123, 'Recoleta', 23);
INSERT INTO COMUNA VALUES(124, 'Renca', 23);
INSERT INTO COMUNA VALUES(125, 'San Miguel', 23);
INSERT INTO COMUNA VALUES(126, 'San Joaquin', 23);
INSERT INTO COMUNA VALUES(127, 'San Ramon', 23);
INSERT INTO COMUNA VALUES(128, 'Santiago', 23);
INSERT INTO COMUNA VALUES(129, 'Vitacura', 23);

INSERT INTO COMUNA VALUES(130, 'El Monte', 27);
INSERT INTO COMUNA VALUES(131, 'Isla de Maipo', 27);
INSERT INTO COMUNA VALUES(132, 'Padre Hurtado', 27);
INSERT INTO COMUNA VALUES(133, 'Penaflor', 27);
INSERT INTO COMUNA VALUES(134, 'Talagante', 27);

INSERT INTO COMUNA VALUES(135, 'Codegua', 28);
INSERT INTO COMUNA VALUES(136, 'Coinco', 28);
INSERT INTO COMUNA VALUES(137, 'Coltauco', 28);
INSERT INTO COMUNA VALUES(138, 'Donihue', 28);
INSERT INTO COMUNA VALUES(139, 'Graneros', 28);
INSERT INTO COMUNA VALUES(140, 'Las Cabras', 28);
INSERT INTO COMUNA VALUES(141, 'Machali', 28);
INSERT INTO COMUNA VALUES(142, 'Malloa', 28);
INSERT INTO COMUNA VALUES(143, 'Mostazal', 28);
INSERT INTO COMUNA VALUES(144, 'Olivar', 28);
INSERT INTO COMUNA VALUES(145, 'Peumo', 28);
INSERT INTO COMUNA VALUES(146, 'Pichidegua', 28);
INSERT INTO COMUNA VALUES(147, 'Quinta de Tilcoco', 28);
INSERT INTO COMUNA VALUES(148, 'Rancagua', 28);
INSERT INTO COMUNA VALUES(149, 'Rengo', 28);
INSERT INTO COMUNA VALUES(150, 'Requinoa', 28);
INSERT INTO COMUNA VALUES(151, 'San Vicente de Tagua Tagua', 28);

INSERT INTO COMUNA VALUES(152, 'La Estrella', 30);
INSERT INTO COMUNA VALUES(153, 'Litueche', 30);
INSERT INTO COMUNA VALUES(154, 'Marchigne', 30);
INSERT INTO COMUNA VALUES(155, 'Navidad', 30);
INSERT INTO COMUNA VALUES(156, 'Paredones', 30);
INSERT INTO COMUNA VALUES(157, 'Pichilemu', 30);

INSERT INTO COMUNA VALUES(158, 'Chepica', 29);
INSERT INTO COMUNA VALUES(159, 'Chimbarongo', 29);
INSERT INTO COMUNA VALUES(160, 'Lolol', 29);
INSERT INTO COMUNA VALUES(161, 'Nancagua', 29);
INSERT INTO COMUNA VALUES(162, 'Palmilla', 29);
INSERT INTO COMUNA VALUES(163, 'Peralillo', 29);
INSERT INTO COMUNA VALUES(164, 'Placilla', 29);
INSERT INTO COMUNA VALUES(165, 'Pumanque', 29);
INSERT INTO COMUNA VALUES(166, 'San Fernando', 29);
INSERT INTO COMUNA VALUES(167, 'Santa Cruz', 29);

INSERT INTO COMUNA VALUES(168, 'Cauquenes', 34);
INSERT INTO COMUNA VALUES(169, 'Chanco', 34);
INSERT INTO COMUNA VALUES(170, 'Pelluhue', 34);

INSERT INTO COMUNA VALUES(171, 'Curico', 31);
INSERT INTO COMUNA VALUES(172, 'Hualane', 31);
INSERT INTO COMUNA VALUES(173, 'Licanten', 31);
INSERT INTO COMUNA VALUES(174, 'Molina', 31);
INSERT INTO COMUNA VALUES(175, 'Rauco', 31);
INSERT INTO COMUNA VALUES(176, 'Romeral', 31);
INSERT INTO COMUNA VALUES(177, 'Sagrada Familia', 31);
INSERT INTO COMUNA VALUES(178, 'Teno', 31);
INSERT INTO COMUNA VALUES(179, 'Vichuquen', 31);

INSERT INTO COMUNA VALUES(180, 'Colbun', 33);
INSERT INTO COMUNA VALUES(181, 'Linares', 33);
INSERT INTO COMUNA VALUES(182, 'Longavi', 33);
INSERT INTO COMUNA VALUES(183, 'Parral', 33);
INSERT INTO COMUNA VALUES(184, 'Retiro', 33);
INSERT INTO COMUNA VALUES(185, 'San Javier', 33);
INSERT INTO COMUNA VALUES(186, 'Villa Alegre', 33);
INSERT INTO COMUNA VALUES(187, 'Yerbas Buenas', 33);

INSERT INTO COMUNA VALUES(188, 'Constitucion', 32);
INSERT INTO COMUNA VALUES(189, 'Curepto', 32);
INSERT INTO COMUNA VALUES(190, 'Empedrado', 32);
INSERT INTO COMUNA VALUES(191, 'Maule', 32);
INSERT INTO COMUNA VALUES(192, 'Pelarco', 32);
INSERT INTO COMUNA VALUES(193, 'Pencahue', 32);
INSERT INTO COMUNA VALUES(194, 'Rio Claro', 32);
INSERT INTO COMUNA VALUES(195, 'San Clemente', 32);
INSERT INTO COMUNA VALUES(196, 'San Rafael', 32);
INSERT INTO COMUNA VALUES(197, 'Talca', 32);

INSERT INTO COMUNA VALUES(198, 'Cobquecura', 36);
INSERT INTO COMUNA VALUES(199, 'Coelemu', 36);
INSERT INTO COMUNA VALUES(200, 'Ninhue', 36);
INSERT INTO COMUNA VALUES(201, 'Portezuelo', 36);
INSERT INTO COMUNA VALUES(202, 'Quirihue', 36);
INSERT INTO COMUNA VALUES(203, 'Ranquil', 36);
INSERT INTO COMUNA VALUES(204, 'Trehuaco', 36);

INSERT INTO COMUNA VALUES(205, 'Bulnes', 35);
INSERT INTO COMUNA VALUES(206, 'Chillan Viejo', 35);
INSERT INTO COMUNA VALUES(207, 'Chillan', 35);
INSERT INTO COMUNA VALUES(208, 'El Carmen', 35);
INSERT INTO COMUNA VALUES(209, 'Pemuco', 35);
INSERT INTO COMUNA VALUES(210, 'Quillon', 35);
INSERT INTO COMUNA VALUES(211, 'Pinto', 35);
INSERT INTO COMUNA VALUES(212, 'San Ignacio', 35);
INSERT INTO COMUNA VALUES(213, 'Yungay', 35);

INSERT INTO COMUNA VALUES(214, 'San Nicolas', 37);
INSERT INTO COMUNA VALUES(215, 'San Fabian', 37);
INSERT INTO COMUNA VALUES(216, 'San Carlos', 37);
INSERT INTO COMUNA VALUES(217, 'Niquen', 37);
INSERT INTO COMUNA VALUES(218, 'Coihueco', 37);

INSERT INTO COMUNA VALUES(219, 'Arauco', 40);
INSERT INTO COMUNA VALUES(220, 'Canete', 40);
INSERT INTO COMUNA VALUES(221, 'Contulmo', 40);
INSERT INTO COMUNA VALUES(222, 'Curanilahue', 40);
INSERT INTO COMUNA VALUES(223, 'Lebu', 40);
INSERT INTO COMUNA VALUES(224, 'Los Alamos', 40);
INSERT INTO COMUNA VALUES(225, 'Tirua', 40);

INSERT INTO COMUNA VALUES(226, 'Alto Biobio', 38);
INSERT INTO COMUNA VALUES(227, 'Antuco', 38);
INSERT INTO COMUNA VALUES(228, 'Cabrero', 38);
INSERT INTO COMUNA VALUES(229, 'Laja', 38);
INSERT INTO COMUNA VALUES(230, 'Los Angeles', 38);
INSERT INTO COMUNA VALUES(231, 'Mulchen', 38);
INSERT INTO COMUNA VALUES(232, 'Nacimiento', 38);
INSERT INTO COMUNA VALUES(233, 'Negrete', 38);
INSERT INTO COMUNA VALUES(234, 'Quilaco', 38);
INSERT INTO COMUNA VALUES(235, 'Quilleco', 38);
INSERT INTO COMUNA VALUES(236, 'San Rosendo', 38);
INSERT INTO COMUNA VALUES(237, 'Santa Barbara', 38);
INSERT INTO COMUNA VALUES(238, 'Tucapel', 38);
INSERT INTO COMUNA VALUES(239, 'Yumbel', 38);

INSERT INTO COMUNA VALUES(240, 'Chiguayante', 39);
INSERT INTO COMUNA VALUES(241, 'Concepcion', 39);
INSERT INTO COMUNA VALUES(242, 'Coronel', 39);
INSERT INTO COMUNA VALUES(243, 'Florida', 39);
INSERT INTO COMUNA VALUES(244, 'Hualpen', 39);
INSERT INTO COMUNA VALUES(245, 'Hualqui', 39);
INSERT INTO COMUNA VALUES(246, 'Lota', 39);
INSERT INTO COMUNA VALUES(247, 'Penco', 39);
INSERT INTO COMUNA VALUES(248, 'San Pedro de la Paz', 39);
INSERT INTO COMUNA VALUES(249, 'Santa Juana', 39);
INSERT INTO COMUNA VALUES(250, 'Talcahuano', 39);
INSERT INTO COMUNA VALUES(251, 'Tome', 39);

INSERT INTO COMUNA VALUES(252, 'Carahue', 42);
INSERT INTO COMUNA VALUES(253, 'Cholchol', 42);
INSERT INTO COMUNA VALUES(254, 'Cunco', 42);
INSERT INTO COMUNA VALUES(255, 'Curarrehue', 42);
INSERT INTO COMUNA VALUES(256, 'Freire', 42);
INSERT INTO COMUNA VALUES(257, 'Galvarino', 42);
INSERT INTO COMUNA VALUES(258, 'Gorbea', 42);
INSERT INTO COMUNA VALUES(259, 'Lautaro', 42);
INSERT INTO COMUNA VALUES(260, 'Loncoche', 42);
INSERT INTO COMUNA VALUES(261, 'Melipeuco', 42);
INSERT INTO COMUNA VALUES(262, 'Nueva Imperial', 42);
INSERT INTO COMUNA VALUES(263, 'Padre Las Casas', 42);
INSERT INTO COMUNA VALUES(264, 'Perquenco', 42);
INSERT INTO COMUNA VALUES(265, 'Pitrufquen', 42);
INSERT INTO COMUNA VALUES(266, 'Pucon', 42);
INSERT INTO COMUNA VALUES(267, 'Puerto Saavedra', 42);
INSERT INTO COMUNA VALUES(268, 'Temuco', 42);
INSERT INTO COMUNA VALUES(269, 'Teodoro Schmidt', 42);
INSERT INTO COMUNA VALUES(270, 'Tolten', 42);
INSERT INTO COMUNA VALUES(271, 'Vilcun', 42);
INSERT INTO COMUNA VALUES(272, 'Villarrica', 42);

INSERT INTO COMUNA VALUES(273, 'Angol', 41);
INSERT INTO COMUNA VALUES(274, 'Collipulli', 41);
INSERT INTO COMUNA VALUES(275, 'Curacautin', 41);
INSERT INTO COMUNA VALUES(276, 'Ercilla', 41);
INSERT INTO COMUNA VALUES(277, 'Lonquimay', 41);
INSERT INTO COMUNA VALUES(278, 'Los Sauces', 41);
INSERT INTO COMUNA VALUES(279, 'Lumaco', 41);
INSERT INTO COMUNA VALUES(280, 'Puren', 41);
INSERT INTO COMUNA VALUES(281, 'Renaico', 41);
INSERT INTO COMUNA VALUES(282, 'Traiguen', 41);
INSERT INTO COMUNA VALUES(283, 'Victoria', 41);

INSERT INTO COMUNA VALUES(284, 'Mariquina', 43);
INSERT INTO COMUNA VALUES(285, 'Lanco', 43);
INSERT INTO COMUNA VALUES(286, 'Mafil', 43);
INSERT INTO COMUNA VALUES(287, 'Valdivia', 43);
INSERT INTO COMUNA VALUES(288, 'Corral', 43);
INSERT INTO COMUNA VALUES(289, 'Paillaco', 43);
INSERT INTO COMUNA VALUES(290, 'Los Lagos', 43);
INSERT INTO COMUNA VALUES(291, 'Panguipulli', 43);

INSERT INTO COMUNA VALUES(292, 'La Union', 44);
INSERT INTO COMUNA VALUES(293, 'Rio Bueno', 44);
INSERT INTO COMUNA VALUES(294, 'Lago Ranco', 44);
INSERT INTO COMUNA VALUES(295, 'Futrono', 44);

INSERT INTO COMUNA VALUES(296, 'Ancud', 47);
INSERT INTO COMUNA VALUES(297, 'Castro', 47);
INSERT INTO COMUNA VALUES(298, 'Chonchi', 47);
INSERT INTO COMUNA VALUES(299, 'Curaco de Velez', 47);
INSERT INTO COMUNA VALUES(300, 'Dalcahue', 47);
INSERT INTO COMUNA VALUES(301, 'Puqueldon', 47);
INSERT INTO COMUNA VALUES(302, 'Queilen', 47);
INSERT INTO COMUNA VALUES(303, 'Quemchi', 47);
INSERT INTO COMUNA VALUES(304, 'Quellon', 47);
INSERT INTO COMUNA VALUES(305, 'Quinchao', 47);

INSERT INTO COMUNA VALUES(306, 'Calbuco', 46);
INSERT INTO COMUNA VALUES(307, 'Cochamo', 46);
INSERT INTO COMUNA VALUES(308, 'Fresia', 46);
INSERT INTO COMUNA VALUES(309, 'Frutillar', 46);
INSERT INTO COMUNA VALUES(310, 'Llanquihue', 46);
INSERT INTO COMUNA VALUES(311, 'Los Muermos', 46);
INSERT INTO COMUNA VALUES(312, 'Maullin', 46);
INSERT INTO COMUNA VALUES(313, 'Puerto Montt', 46);
INSERT INTO COMUNA VALUES(314, 'Puerto Varas', 46);

INSERT INTO COMUNA VALUES(315, 'Osorno', 45);
INSERT INTO COMUNA VALUES(316, 'Puerto Octay', 45);
INSERT INTO COMUNA VALUES(317, 'Purranque', 45);
INSERT INTO COMUNA VALUES(318, 'Puyehue', 45);
INSERT INTO COMUNA VALUES(319, 'Rio Negro', 45);
INSERT INTO COMUNA VALUES(320, 'San Juan de la Costa', 45);
INSERT INTO COMUNA VALUES(321, 'San Pablo', 45);

INSERT INTO COMUNA VALUES(322, 'Chaiten', 48);
INSERT INTO COMUNA VALUES(323, 'Futaleufu', 48);
INSERT INTO COMUNA VALUES(324, 'Hualaihue', 48);
INSERT INTO COMUNA VALUES(325, 'Palena', 48);

INSERT INTO COMUNA VALUES(326, 'Cisnes', 50);
INSERT INTO COMUNA VALUES(327, 'Guaitecas', 50);
INSERT INTO COMUNA VALUES(328, 'Aysen', 50);

INSERT INTO COMUNA VALUES(329, 'Cochrane', 52);
INSERT INTO COMUNA VALUES(330, 'O Higgins', 52);
INSERT INTO COMUNA VALUES(331, 'Tortel', 52);

INSERT INTO COMUNA VALUES(332, 'Coyhaique', 49);
INSERT INTO COMUNA VALUES(333, 'Lago Verde', 49);

INSERT INTO COMUNA VALUES(334, 'Chile Chico', 51);
INSERT INTO COMUNA VALUES(335, 'Rio Ibanez', 51);

INSERT INTO COMUNA VALUES(336, 'Antartica', 56);
INSERT INTO COMUNA VALUES(337, 'Cabo de Hornos', 56);

INSERT INTO COMUNA VALUES(338, 'Laguna Blanca', 54);
INSERT INTO COMUNA VALUES(339, 'Punta Arenas', 54);
INSERT INTO COMUNA VALUES(340, 'Rio Verde', 54);
INSERT INTO COMUNA VALUES(341, 'San Gregorio', 54);

INSERT INTO COMUNA VALUES(342, 'Porvenir', 55);
INSERT INTO COMUNA VALUES(343, 'Primavera', 55);
INSERT INTO COMUNA VALUES(344, 'Timaukel', 55);

INSERT INTO COMUNA VALUES(345, 'Natales', 53);
INSERT INTO COMUNA VALUES(346, 'Torres del Paine', 53);

INSERT INTO CATEGORIA VALUES(1, 'Flores');
INSERT INTO CATEGORIA VALUES(2, 'Arboles');
INSERT INTO CATEGORIA VALUES(3, 'Arbustos');
INSERT INTO CATEGORIA VALUES(4, 'Herramientas');