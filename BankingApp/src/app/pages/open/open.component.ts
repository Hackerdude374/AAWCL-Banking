import { Component } from '@angular/core';
import { AccountService } from '../../service/acc.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-open',
  standalone: true,
  imports: [],
  templateUrl: './open.component.html',
  styleUrl: './open.component.css'
})
export class OpenComponent {
  openStatus!: string;

  constructor(private accountService: AccountService, private router: Router) { }

  openAccount(accountType: string) {
    this.accountService.openAccount(accountType).subscribe(
      (response) => {
        console.log('Account opened successfully:', response);
        this.openStatus = 'Account opened successfully';
        this.router.navigate(['/dashboard']);
      },
      (error) => {
        console.error('Error opening account:', error);
        this.openStatus = error;
      }
    );
  }

  openCard(cardType: string) {
    this.accountService.openCard(cardType).subscribe(
      (response) => {
        console.log('Card opened successfully:', response);
        this.openStatus = 'Card opened successfully';
        this.router.navigate(['/dashboard']);
      },
      (error) => {
        console.error('Error opening card:', error);
        this.openStatus = error;
      }
    );
  }
}
