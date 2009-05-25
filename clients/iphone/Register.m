#import "Register.h"

@implementation Register
CGFloat animatedDistance;
static const CGFloat KEYBOARD_ANIMATION_DURATION = 0.3;
static const CGFloat MINIMUM_SCROLL_FRACTION = 0.2;
static const CGFloat MAXIMUM_SCROLL_FRACTION = 0.8;
static const CGFloat PORTRAIT_KEYBOARD_HEIGHT = 216;
static const CGFloat LANDSCAPE_KEYBOARD_HEIGHT = 162;

- (IBAction)sendRegistrationInfo {
    
}
- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event
{
    // Dismiss the keyboard when the view outside the text field is touched.
	//Going through each text box may not be the best way to do this.
	[userName resignFirstResponder];
	[email resignFirstResponder];
	[firstName resignFirstResponder];
	[lastName resignFirstResponder];
	[password resignFirstResponder];
	[confirmPassword resignFirstResponder];
    // Revert the text field to the previous value.
	// textField.text = self.string; 
	// [super touchesBegan:touches withEvent:event];
}

- (void)updateStrings{
	NSLog(userName.text);
	NSLog(email.text);
	NSLog(firstName.text);
	NSLog(lastName.text);
	NSLog(password.text);
	NSLog(confirmPassword.text);
}
- (BOOL)textFieldShouldClear:(UITextField *)textField {
	return NO;
}
- (void)textFieldDidEndEditing:(UITextField *)textField
{
    CGRect viewFrame = self.frame;
    viewFrame.origin.y += animatedDistance;
    
    [UIView beginAnimations:nil context:NULL];
    [UIView setAnimationBeginsFromCurrentState:YES];
    [UIView setAnimationDuration:KEYBOARD_ANIMATION_DURATION];
    
    [self setFrame:viewFrame];
    
    [UIView commitAnimations];
}
//- (BOOL) textFieldShouldReturn:(UITextField *)textField{
//	NSLog(@"text field Should Return");
//	[textField resignFirstResponder];
//	//Begin aniimations to move Text Fields into view
//	[UIView beginAnimations:@"moveField" context:nil];
//	[UIView setAnimationDelegate:self];
//	[UIView setAnimationDuration:0.5];
//	[UIView setAnimationCurve:UIViewAnimationCurveEaseInOut];
//	UIView *a = [UIView alloc];
//	a = [textField delegate];
//	a.frame =CGRectMake(a.frame.origin.x,
//						a.frame.origin.y+100, 
//						a.frame.size.width, 
//						a.frame.size.height);
//	[UIView commitAnimations];
//	[a release];
//	return YES;
//}
- (BOOL) textFieldShouldBeginEditing:(UITextField *)textField{
	{
		CGRect textFieldRect =
        [self.window convertRect:textField.bounds fromView:textField];
		CGRect viewRect =
        [self.window convertRect:self.bounds fromView:self];

		CGFloat midline = textFieldRect.origin.y + 0.5 * textFieldRect.size.height;
		CGFloat numerator =
        midline - viewRect.origin.y
		- MINIMUM_SCROLL_FRACTION * viewRect.size.height;
		CGFloat denominator =
        (MAXIMUM_SCROLL_FRACTION - MINIMUM_SCROLL_FRACTION)
		* viewRect.size.height;
		CGFloat heightFraction = numerator / denominator;
		
		if (heightFraction < 0.0)
		{
			heightFraction = 0.0;
		}
		else if (heightFraction > 1.0)
		{
			heightFraction = 1.0;
		}
		
		animatedDistance = floor(PORTRAIT_KEYBOARD_HEIGHT * heightFraction);
		
		CGRect viewFrame = self.frame;
		viewFrame.origin.y -= animatedDistance;
		
		[UIView beginAnimations:nil context:NULL];
		[UIView setAnimationBeginsFromCurrentState:YES];
		[UIView setAnimationDuration:KEYBOARD_ANIMATION_DURATION];
		
		[self setFrame:viewFrame];
		
		[UIView commitAnimations];
		return YES;
	}
		
		//Begin aniimations to move Text Fields into view
//	[UIView beginAnimations:@"moveField" context:nil];
//	[UIView setAnimationDelegate:self];
//	[UIView setAnimationDuration:0.5];
//	[UIView setAnimationCurve:UIViewAnimationCurveEaseInOut];
//	//UIView *a = [UIView alloc];
//	UIView *a = [textField delegate];
//	a.frame =CGRectMake(a.frame.origin.x,
//								 a.frame.origin.y-100, 
//								 a.frame.size.width, 
//								 a.frame.size.height);
//	[UIView commitAnimations];
//	[a release];
//	return YES;
}

@end
