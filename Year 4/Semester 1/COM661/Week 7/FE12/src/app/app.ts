import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import jsonData from '../assets/businesses.json';

@Component({
  imports: [RouterOutlet],
  selector: 'app-root',
  styleUrl: './app.css',
  templateUrl: './app.html',
})
export class App {
  protected readonly title = signal('FE12');

  ngOnInit() {
    console.log(jsonData);
  }
}

// NOTE: node_modules folder needs redownloaded to access packages and run app