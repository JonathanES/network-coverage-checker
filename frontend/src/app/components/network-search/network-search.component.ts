import { Component, Output, EventEmitter }  from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';

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

    @Output() searchResults = new EventEmitter<any>();

    onSearch() {
      if (!this.addresses.trim()) return;

      const addressList = this.addresses
        .split(';')
        .map(addr => addr.trim())
        .filter(addr => addr.length > 0);

      const requestPayload: AddressRequest = {};
      addressList.forEach((address, index) => {
        requestPayload[`id${index + 1}`] = address;
      });

      console.log('Request payload:', requestPayload);

      // TODO: Replace with actual API call
      const mockResults: any = {};
      Object.keys(requestPayload).forEach(id => {
        mockResults[id] = {
          "orange": {"2G": true, "3G": true, "4G": false},
          "SFR": {"2G": true, "3G": true, "4G": true},
          "bouygues": {"2G": true, "3G": false, "4G": false}
        };
      });

      this.searchResults.emit(mockResults);
    }
}
