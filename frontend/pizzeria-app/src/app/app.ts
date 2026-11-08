
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})

export class App {

  constructor(private http: HttpClient) {}

  
  nombre: string = '';
  direccion: string = '';
  telefono: string = '';

  
  fecha: string = '';
  tamano: string = '';
  jamon: boolean = false;
  pina: boolean = false;
  champinones: boolean = false;
  cantidad: number = 1;

  
  pedidos: any[] = [];
  total: number = 0;
  totalPizzas: number = 0;
  mostrarResumen: boolean = false;

  
  diaConsulta: string = 'lunes';
  mesConsulta: string = 'enero';
  idPedidoConsulta: number = 1;

  ventasConsulta: any[] = [];
  totalConsulta: number = 0;
  tituloConsulta: string = '';
  mostrarVentas: boolean = false;

  detalleVenta: any = null;
  mostrarDetalle: boolean = false;

  
  agregarPedido() {

    if (this.nombre == '' || this.direccion == '' || this.telefono == '') {
      alert('Completa los datos del cliente');
      return;
    }

    if (this.tamano == '' || this.cantidad < 1) {
      alert('Selecciona el tamaño y la cantidad de pizzas');
      return;
    }

    let precio = 0;

    if (this.tamano == 'Chica') {
      precio = 40;
    }

    if (this.tamano == 'Mediana') {
      precio = 80;
    }

    if (this.tamano == 'Grande') {
      precio = 120;
    }

    let precioIngredientes = 0;
    let ingredientes = '';

    if (this.jamon == true) {
      precioIngredientes += 10;
      ingredientes += 'Jamón ';
    }

    if (this.pina == true) {
      precioIngredientes += 10;
      ingredientes += 'Piña ';
    }

    if (this.champinones == true) {
      precioIngredientes += 10;
      ingredientes += 'Champiñones ';
    }

    if (ingredientes == '') {
      ingredientes = 'Sin ingredientes';
    }

    let subtotal = (precio + precioIngredientes) * this.cantidad;

    this.pedidos.push({
      tamano: this.tamano,
      ingredientes: ingredientes,
      cantidad: this.cantidad,
      subtotal: subtotal
    });

    this.calcularTotal();

    this.tamano = '';
    this.jamon = false;
    this.pina = false;
    this.champinones = false;
    this.cantidad = 1;

    this.mostrarResumen = false;

  }

  
  quitarPedido(indice: number) {

    this.pedidos.splice(indice, 1);

    this.calcularTotal();

    this.mostrarResumen = false;

  }

  
  calcularTotal() {

    this.total = 0;
    this.totalPizzas = 0;

    for (let i = 0; i < this.pedidos.length; i++) {
      this.total += this.pedidos[i].subtotal;
      this.totalPizzas += this.pedidos[i].cantidad;
    }

  }

  
  terminarPedido() {

    if (this.nombre == '' || this.direccion == '' || this.telefono == '') {
      alert('Completa los datos del cliente');
      return;
    }

    if (this.pedidos.length == 0) {
      alert('No hay pedidos registrados');
      return;
    }

    let datosPedido = {
      nombre: this.nombre,
      direccion: this.direccion,
      telefono: this.telefono,
      fecha: this.fecha,
      total: this.total
    };

    this.http.post<any>('http://127.0.0.1:5000/pedidos/', datosPedido).subscribe({

      next: (respuesta) => {

        let solicitudes = [];

        for (let i = 0; i < this.pedidos.length; i++) {

          let detalle = {
            pedido_id: respuesta.id,
            tamano: this.pedidos[i].tamano,
            ingredientes: this.pedidos[i].ingredientes,
            cantidad: this.pedidos[i].cantidad,
            subtotal: this.pedidos[i].subtotal
          };

          solicitudes.push(
            this.http.post('http://127.0.0.1:5000/ventas/', detalle)
          );

        }

        forkJoin(solicitudes).subscribe({

          next: () => {
            this.mostrarResumen = true;
            alert('Pedido guardado correctamente en la base de datos');
          },

          error: (error) => {
            console.log(error);
            alert('Error al guardar los detalles del pedido');
          }

        });

      },

      error: (error) => {
        console.log(error);
        alert('Error al registrar el pedido');
      }

    });

  }


  consultarDia() {

    this.http.get<any>(
      'http://127.0.0.1:5000/ventas/dia/' + this.diaConsulta
    ).subscribe({

      next: (respuesta) => {

        this.ventasConsulta = respuesta.ventas;
        this.totalConsulta = respuesta.total_acumulado;
        this.tituloConsulta = 'Ventas del día: ' + this.diaConsulta;

        this.mostrarVentas = true;
        this.mostrarDetalle = false;
        this.detalleVenta = null;

      },

      error: (error) => {
        console.log(error);
        alert('Error al consultar las ventas del día');
      }

    });

  }

  
  consultarMes() {

    this.http.get<any>(
      'http://127.0.0.1:5000/ventas/mes/' + this.mesConsulta
    ).subscribe({

      next: (respuesta) => {

        this.ventasConsulta = respuesta.ventas;
        this.totalConsulta = respuesta.total_acumulado;
        this.tituloConsulta = 'Ventas del mes: ' + this.mesConsulta;

        this.mostrarVentas = true;
        this.mostrarDetalle = false;
        this.detalleVenta = null;

      },

      error: (error) => {
        console.log(error);
        alert('Error al consultar las ventas del mes');
      }

    });

  }

 
  consultarDetalle() {

    if (this.idPedidoConsulta < 1) {
      alert('Ingresa un número de pedido válido');
      return;
    }

    this.http.get<any>(
      'http://127.0.0.1:5000/ventas/detalle/' + this.idPedidoConsulta
    ).subscribe({

      next: (respuesta) => {

        this.detalleVenta = respuesta;

        this.mostrarDetalle = true;
        this.mostrarVentas = false;

      },

      error: (error) => {
        console.log(error);
        this.detalleVenta = null;
        this.mostrarDetalle = false;
        alert('No se encontró el pedido o ocurrió un error en la consulta');
      }

    });

  }

  
  imprimirComprobante() {
    window.print();
  }

  
  nuevoPedido() {

    this.nombre = '';
    this.direccion = '';
    this.telefono = '';
    this.fecha = '';
    this.tamano = '';
    this.jamon = false;
    this.pina = false;
    this.champinones = false;
    this.cantidad = 1;

    this.pedidos = [];
    this.total = 0;
    this.totalPizzas = 0;
    this.mostrarResumen = false;

  }

}
