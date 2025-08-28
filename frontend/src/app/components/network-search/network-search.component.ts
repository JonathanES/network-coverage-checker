import { Component, Output, EventEmitter }  from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { HttpClient } from '@angular/common/http';

interface AddressRequest {
  [addressId: string]: string;
}

  @Component({
    selector: 'app-network-search',
    standalone: true,
    imports: [
      CommonModule,
      FormsModule,
      MatInputModule,
      MatButtonModule,
      MatFormFieldModule
    ],
    templateUrl: './network-search.component.html',
    styleUrl: './network-search.component.css'
  })
  export class NetworkSearchComponent {
    addresses: string = '';
    errorMessage: string = '';

    @Output() searchResults = new EventEmitter<any>();
    @Output() error = new EventEmitter<string>();

    constructor(private http: HttpClient) {}

    onSearch() {
      if (!this.addresses.trim()) return;

      const addressList = this.addresses
        .split(';')
        .map(addr => addr.trim())
        .filter(addr => addr.length > 0);

      const requestPayload: AddressRequest = {};
      const addressMapping: { [uuid: string]: string } = {};

      addressList.forEach((address) => {
        const uuid = crypto.randomUUID();
        requestPayload[uuid] = address;
        addressMapping[uuid] = address;
      });

      this.errorMessage = '';

      this.http.post<any>('http://localhost:8000/api/v1/coverage', requestPayload)
        .subscribe({
          next: (results) => {
            this.errorMessage = '';

            const resultsWithAddresses = { ...results, _addressMapping: addressMapping };
            this.searchResults.emit(resultsWithAddresses);
          },
          error: (error) => {
            console.error('API error:', error);
            const errorMsg = `Failed to get coverage data: ${error.message || 'Network error'}`;
            this.errorMessage = errorMsg;
            this.error.emit(errorMsg);
          }
        });
    }
}
