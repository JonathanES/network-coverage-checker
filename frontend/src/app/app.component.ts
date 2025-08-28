import { Component } from '@angular/core';
import { NetworkSearchComponent } from './components/network-search/network-search.component';
import { NetworkResultsComponent } from './components/network-results/network-results.component';

@Component({
  selector: 'app-root',
  imports: [NetworkSearchComponent, NetworkResultsComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'frontend';
  searchResults: any = null;

  onSearchResults(results: any) {
    this.searchResults = results;
  }
}
