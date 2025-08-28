import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';

interface NetworkTypeCoverage {
  [networkType: string]: boolean;
}

interface OperatorCoverage {
  [operatorName: string]: NetworkTypeCoverage;
}

interface LocationCoverageData {
  error: string | null;
  operators: OperatorCoverage;
}

interface NetworkResults {
  [addressId: string]: LocationCoverageData;
}

type NetworkResultsWithMapping = NetworkResults & {
  _addressMapping?: { [uuid: string]: string };
}

@Component({
  selector: 'app-network-results',
  imports: [CommonModule, MatCardModule],
  templateUrl: './network-results.component.html',
  styleUrl: './network-results.component.css'
})
export class NetworkResultsComponent {
  @Input() results: NetworkResultsWithMapping | null = null;

  get operators(): string[] {
    if (!this.results) return [];
    const addressIds = this.addresses;
    if (addressIds.length === 0) return [];
    const firstAddressData = this.results[addressIds[0]];
    if (!firstAddressData || firstAddressData.error) return [];
    return Object.keys(firstAddressData.operators || {});
  }

  get addresses(): string[] {
    if (!this.results) return [];
    return Object.keys(this.results).filter(key => key !== '_addressMapping');
  }

  get networkTypes(): string[] {
    if (!this.results) return [];
    const addressIds = this.addresses;
    if (addressIds.length === 0) return [];
    const firstAddressData = this.results[addressIds[0]];
    if (!firstAddressData || firstAddressData.error || !firstAddressData.operators) return [];
    const firstOperator = Object.values(firstAddressData.operators)[0];
    return Object.keys(firstOperator || {});
  }

  getStatusText(status: boolean): string {
    return status ? 'OK' : 'KO';
  }

  getCoverage(addressId: string, operator: string, networkType: string): boolean {
    return this.results?.[addressId]?.operators?.[operator]?.[networkType] || false;
  }

  hasError(addressId: string): boolean {
    return !!this.results?.[addressId]?.error;
  }

  getError(addressId: string): string | null {
    return this.results?.[addressId]?.error || null;
  }

  getDisplayAddress(addressId: string): string {
    return this.results?._addressMapping?.[addressId] || addressId;
  }
}
